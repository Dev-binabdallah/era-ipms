import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    activity_assignment_create,
    activity_assignment_update,
    activity_assignments,
)


class ActivityAssignmentsApiTests(SimpleTestCase):
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

        self.activity = SimpleNamespace(
            activity_id=1,
            project=SimpleNamespace(project_id=100),
        )

    def make_get_request(
        self,
        user,
        path="/activities/1/assignments/",
    ):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_post_request(
        self,
        user,
        path="/activities/1/assignments/create/",
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
        path="/activities/1/assignments/5/",
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
        response = activity_assignments(
            self.make_get_request(self.unauthenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_assign_activity.assert_not_called()

    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_unauthorized_returns_403(
        self,
        service,
        activity_get,
    ):
        service.can_assign_activity.return_value = False
        activity_get.return_value = self.activity

        response = activity_assignments(
            self.make_get_request(self.authenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_assign_activity.assert_called_once_with(
            self.authenticated_user,
            self.activity,
        )

    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_missing_activity_returns_404(
        self,
        service,
        activity_get,
    ):
        from core.models import Activities

        activity_get.side_effect = Activities.DoesNotExist

        response = activity_assignments(
            self.make_get_request(self.authenticated_user),
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Activity not found"},
        )

        service.can_assign_activity.assert_not_called()

    @patch("core.views.ActivityAssignments.objects.filter")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_returns_assignments(
        self,
        service,
        activity_get,
        assignments_filter,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        assignment = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="2026-09-08T10:00:00Z",
            assigned_by_id=10,
            status="assigned",
        )

        assignments_filter.return_value = [assignment]

        response = activity_assignments(
            self.make_get_request(self.authenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignments": [
                    {
                        "activity_assignment_id": 5,
                        "activity_id": 1,
                        "user_id": 20,
                        "assigned_at": "2026-09-08T10:00:00Z",
                        "assigned_by_id": 10,
                        "status": "assigned",
                    }
                ]
            },
        )

        assignments_filter.assert_called_once_with(
            activity=self.activity,
        )

    @patch("core.views.ActivityAssignments.objects.create")
    @patch("core.views.ActivityAssignments.objects.filter")
    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_creates_assignment(
        self,
        service,
        activity_get,
        user_get,
        assignments_filter,
        assignment_create,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        target_user = SimpleNamespace(
            user_id=20,
            is_active=True,
        )

        assignment = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="2026-09-08T10:00:00Z",
            assigned_by_id=10,
            status="assigned",
        )

        user_get.return_value = target_user
        assignments_filter.return_value.first.return_value = None
        assignment_create.return_value = assignment

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"user_id":20}',
        )

        with patch(
            "django.utils.timezone.now",
            return_value="2026-09-08T10:00:00Z",
        ):
            response = activity_assignment_create(
                request,
                1,
            )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "activity_assignment_id": 5,
                    "activity_id": 1,
                    "user_id": 20,
                    "assigned_at": "2026-09-08T10:00:00Z",
                    "assigned_by_id": 10,
                    "status": "assigned",
                }
            },
        )

        assignment_create.assert_called_once()

        create_kwargs = assignment_create.call_args.kwargs
        self.assertEqual(create_kwargs["activity"], self.activity)
        self.assertEqual(create_kwargs["user"], target_user)
        self.assertEqual(
            create_kwargs["assigned_by"],
            self.authenticated_user,
        )
        self.assertEqual(
            create_kwargs["assigned_at"],
            "2026-09-08T10:00:00Z",
        )
        self.assertEqual(create_kwargs["status"], "assigned")

    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_user_id_returns_400(
        self,
        service,
        activity_get,
        user_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        response = activity_assignment_create(
            self.make_post_request(
                self.authenticated_user,
                body=b"{}",
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "user_id is required"},
        )

        user_get.assert_not_called()

    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_user_id_returns_400(
        self,
        service,
        activity_get,
        user_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        response = activity_assignment_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"user_id":"abc"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "user_id must be an integer"},
        )

        user_get.assert_not_called()

    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_nonpositive_user_id_returns_400(
        self,
        service,
        activity_get,
        user_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        response = activity_assignment_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"user_id":0}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "user_id must be a positive integer"},
        )

        user_get.assert_not_called()

    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_target_user_returns_404(
        self,
        service,
        activity_get,
        user_get,
    ):
        from core.models import Users

        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity
        user_get.side_effect = Users.DoesNotExist

        response = activity_assignment_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"user_id":999}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Target user not found"},
        )

    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_inactive_target_user_returns_400(
        self,
        service,
        activity_get,
        user_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        user_get.return_value = SimpleNamespace(
            user_id=20,
            is_active=False,
        )

        response = activity_assignment_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"user_id":20}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Target user is inactive"},
        )

    @patch("core.views.ActivityAssignments.objects.filter")
    @patch("core.views.Users.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_reactivates_existing_assignment(
        self,
        service,
        activity_get,
        user_get,
        assignments_filter,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        target_user = SimpleNamespace(
            user_id=20,
            is_active=True,
        )

        assignment = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="old-time",
            assigned_by_id=10,
            status="completed",
            save=Mock(),
        )

        user_get.return_value = target_user
        assignments_filter.return_value.first.return_value = assignment

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"user_id":20}',
        )

        with patch(
            "django.utils.timezone.now",
            return_value="2026-09-08T11:00:00Z",
        ):
            response = activity_assignment_create(
                request,
                1,
            )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "activity_assignment_id": 5,
                    "activity_id": 1,
                    "user_id": 20,
                    "assigned_at": "2026-09-08T11:00:00Z",
                    "assigned_by_id": 10,
                    "status": "assigned",
                }
            },
        )

        self.assertEqual(assignment.status, "assigned")
        self.assertEqual(
            assignment.assigned_at,
            "2026-09-08T11:00:00Z",
        )
        self.assertEqual(
            assignment.assigned_by,
            self.authenticated_user,
        )

        assignment.save.assert_called_once_with(
            update_fields=[
                "status",
                "assigned_at",
                "assigned_by",
            ],
        )

        assignments_filter.assert_called_once_with(
            user=target_user,
            activity=self.activity,
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_missing_assignment_returns_404(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        from core.models import ActivityAssignments

        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity
        assignment_get.side_effect = ActivityAssignments.DoesNotExist

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"completed"}',
            ),
            1,
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Activity assignment not found"},
        )

        assignment_get.assert_called_once_with(
            activity_assignment_id=999,
            activity=self.activity,
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_authorized_changes_status(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        assignment = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="2026-09-08T10:00:00Z",
            assigned_by_id=10,
            status="assigned",
            save=Mock(),
        )

        assignment_get.return_value = assignment

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"completed"}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "activity_assignment_id": 5,
                    "activity_id": 1,
                    "user_id": 20,
                    "assigned_at": "2026-09-08T10:00:00Z",
                    "assigned_by_id": 10,
                    "status": "completed",
                }
            },
        )

        self.assertEqual(assignment.status, "completed")
        assignment.save.assert_called_once_with(
            update_fields=["status"],
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_rejects_unexpected_fields(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"completed","user_id":20}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Only status can be modified"},
        )

        assignment_get.assert_called_once_with(
            activity_assignment_id=5,
            activity=self.activity,
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_missing_status_returns_400(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Request body is required"},
        )

        assignment_get.assert_called_once_with(
            activity_assignment_id=5,
            activity=self.activity,
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_empty_status_returns_400(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity
        assignment_get.return_value = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="2026-09-08T10:00:00Z",
            assigned_by_id=10,
            status="assigned",
            save=Mock(),
        )

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"   "}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "status must be a non-empty string"},
        )

    @patch("core.views.ActivityAssignments.objects.get")
    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_status_returns_400(
        self,
        service,
        activity_get,
        assignment_get,
    ):
        service.can_assign_activity.return_value = True
        activity_get.return_value = self.activity

        assignment = SimpleNamespace(
            activity_assignment_id=5,
            activity_id=1,
            user_id=20,
            assigned_at="2026-09-08T10:00:00Z",
            assigned_by_id=10,
            status="assigned",
            save=Mock(),
        )

        assignment_get.return_value = assignment

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"unknown"}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "status must be one of: "
                    "assigned, completed, cancelled"
                )
            },
        )

        self.assertEqual(assignment.status, "assigned")
        assignment.save.assert_not_called()


    @patch("core.models.Activities.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_unauthorized_returns_403(
        self,
        service,
        activity_get,
    ):
        service.can_assign_activity.return_value = False
        activity_get.return_value = self.activity

        response = activity_assignment_update(
            self.make_patch_request(
                self.authenticated_user,
                body=b'{"status":"completed"}',
            ),
            1,
            5,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_assign_activity.assert_called_once_with(
            self.authenticated_user,
            self.activity,
        )

    def test_method_restrictions(self):
        activity = self.activity

        with patch(
            "core.models.Activities.objects.get",
            return_value=activity,
        ), patch(
            "core.authorization.decorators.authorization_service"
        ) as service:
            service.can_assign_activity.return_value = True

            post_response = activity_assignments(
                self.make_post_request(self.authenticated_user),
                1,
            )

            get_response = activity_assignment_create(
                self.make_get_request(self.authenticated_user),
                1,
            )

            post_update_response = activity_assignment_update(
                self.make_post_request(self.authenticated_user),
                1,
                5,
            )

        self.assertEqual(post_response.status_code, 405)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(post_update_response.status_code, 405)
