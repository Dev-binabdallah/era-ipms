from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase

from core.authorization.constants import (
    PERMISSION_ADD,
    PERMISSION_APPROVE,
    PERMISSION_VIEW,
    RESPONSIBILITY_BENEFICIARY_REGISTRATION,
    RESPONSIBILITY_FINANCIAL_OPERATIONS,
    RESPONSIBILITY_PROJECT_COORDINATION,
    RESPONSIBILITY_PROJECT_ACTIVITIES,
)
from core.authorization.service import AuthorizationService


class AuthorizationServicePermissionTests(SimpleTestCase):
    def setUp(self):
        self.service = AuthorizationService()

    def make_user(
        self,
        *,
        authenticated=True,
        active=True,
        title_name="Programme Coordinator",
        title_active=True,
        permissions=None,
        responsibilities=None,
    ):
        permission_codes = set(permissions or [])
        responsibility_codes = set(responsibilities or [])

        title_permissions = Mock()

        def permission_filter(**kwargs):
            permission_code = kwargs.get(
                "permission__permission_code"
            )
            result = Mock()
            result.exists.return_value = (
                permission_code in permission_codes
            )
            return result

        title_permissions.filter.side_effect = permission_filter

        title = SimpleNamespace(
            title_name=title_name,
            is_active=title_active,
            title_permissions=title_permissions,
        )

        responsibility_assignments = Mock()

        def responsibility_filter(**kwargs):
            responsibility_code = kwargs.get(
                "responsibility__responsibility_code"
            )
            is_active = kwargs.get("is_active")

            result = Mock()
            result.exists.return_value = (
                responsibility_code in responsibility_codes
                and is_active is True
            )
            return result

        responsibility_assignments.filter.side_effect = (
            responsibility_filter
        )

        return SimpleNamespace(
            is_authenticated=authenticated,
            is_active=active,
            title=title,
            responsibility_assignments=responsibility_assignments,
        )

    def test_unauthenticated_user_is_denied(self):
        user = self.make_user(
            authenticated=False,
            permissions={PERMISSION_VIEW},
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_VIEW)
        )

    def test_inactive_user_is_denied(self):
        user = self.make_user(
            active=False,
            permissions={PERMISSION_VIEW},
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_VIEW)
        )

    def test_user_without_title_is_denied(self):
        user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            title=None,
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_VIEW)
        )

    def test_inactive_title_is_denied(self):
        user = self.make_user(
            title_active=False,
            permissions={PERMISSION_VIEW},
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_VIEW)
        )

    def test_assigned_permission_is_allowed(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
        )

        self.assertTrue(
            self.service.has_permission(user, PERMISSION_VIEW)
        )

    def test_unassigned_permission_is_denied(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_ADD)
        )

    def test_approve_is_independent_from_edit_or_view(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW, PERMISSION_ADD},
        )

        self.assertFalse(
            self.service.has_permission(user, PERMISSION_APPROVE)
        )


class AuthorizationServiceResponsibilityTests(SimpleTestCase):
    def setUp(self):
        self.service = AuthorizationService()

    def make_user(
        self,
        *,
        title_name="Programme Coordinator",
        authenticated=True,
        active=True,
        title_active=True,
        responsibilities=None,
    ):
        responsibility_codes = set(responsibilities or [])

        assignments = Mock()

        def filter_side_effect(**kwargs):
            responsibility_code = kwargs.get(
                "responsibility__responsibility_code"
            )
            is_active = kwargs.get("is_active")

            result = Mock()
            result.exists.return_value = (
                responsibility_code in responsibility_codes
                and is_active is True
            )
            return result

        assignments.filter.side_effect = filter_side_effect

        title = SimpleNamespace(
            title_name=title_name,
            is_active=title_active,
        )

        return SimpleNamespace(
            is_authenticated=authenticated,
            is_active=active,
            title=title,
            responsibility_assignments=assignments,
        )

    def test_eligible_active_responsibility_is_allowed(self):
        user = self.make_user(
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION
            },
        )

        self.assertTrue(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_missing_responsibility_assignment_is_denied(self):
        user = self.make_user()

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_inactive_assignment_is_denied(self):
        user = self.make_user(
            responsibilities=set(),
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_ineligible_title_is_denied(self):
        user = self.make_user(
            title_name="Finance",
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_finance_can_have_financial_responsibility(self):
        user = self.make_user(
            title_name="Finance",
            responsibilities={
                RESPONSIBILITY_FINANCIAL_OPERATIONS,
            },
        )

        self.assertTrue(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_FINANCIAL_OPERATIONS,
            )
        )

    def test_member_cannot_have_project_coordination_responsibility(self):
        user = self.make_user(
            title_name="Member",
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_PROJECT_COORDINATION,
            )
        )

    def test_admin_has_no_programme_responsibilities(self):
        user = self.make_user(
            title_name="Admin",
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_unauthenticated_user_is_denied(self):
        user = self.make_user(
            authenticated=False,
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_inactive_user_is_denied(self):
        user = self.make_user(
            active=False,
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_inactive_title_is_denied(self):
        user = self.make_user(
            title_active=False,
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.has_responsibility(
                user,
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            )
        )

    def test_unknown_responsibility_is_denied(self):
        user = self.make_user()

        self.assertFalse(
            self.service.has_responsibility(
                user,
                "NOT_A_REAL_RESPONSIBILITY",
            )
        )


class AuthorizationServiceResourceMappingTests(SimpleTestCase):
    def setUp(self):
        self.service = AuthorizationService()

    def test_beneficiary_requires_beneficiary_registration(self):
        from core.authorization.constants import (
            RESPONSIBILITY_BENEFICIARY_REGISTRATION,
        )

        self.assertEqual(
            self.service.get_required_responsibility("beneficiary"),
            RESPONSIBILITY_BENEFICIARY_REGISTRATION,
        )

    def test_project_requires_project_coordination(self):
        from core.authorization.constants import (
            RESPONSIBILITY_PROJECT_COORDINATION,
        )

        self.assertEqual(
            self.service.get_required_responsibility("project"),
            RESPONSIBILITY_PROJECT_COORDINATION,
        )

    def test_activity_requires_project_activities(self):
        from core.authorization.constants import (
            RESPONSIBILITY_PROJECT_ACTIVITIES,
        )

        self.assertEqual(
            self.service.get_required_responsibility("activity"),
            RESPONSIBILITY_PROJECT_ACTIVITIES,
        )

    def test_financial_transaction_requires_financial_operations(self):
        from core.authorization.constants import (
            RESPONSIBILITY_FINANCIAL_OPERATIONS,
        )

        self.assertEqual(
            self.service.get_required_responsibility(
                "financial_transaction"
            ),
            RESPONSIBILITY_FINANCIAL_OPERATIONS,
        )

    def test_farm_requires_farm_operations(self):
        from core.authorization.constants import (
            RESPONSIBILITY_FARM_OPERATIONS,
        )

        self.assertEqual(
            self.service.get_required_responsibility("farm"),
            RESPONSIBILITY_FARM_OPERATIONS,
        )

    def test_poultry_group_requires_poultry_operations(self):
        from core.authorization.constants import (
            RESPONSIBILITY_POULTRY_OPERATIONS,
        )

        self.assertEqual(
            self.service.get_required_responsibility("poultry_group"),
            RESPONSIBILITY_POULTRY_OPERATIONS,
        )

    def test_me_indicator_requires_monitoring_evaluation(self):
        from core.authorization.constants import (
            RESPONSIBILITY_MONITORING_EVALUATION,
        )

        self.assertEqual(
            self.service.get_required_responsibility("me_indicator"),
            RESPONSIBILITY_MONITORING_EVALUATION,
        )

    def test_plural_resource_name_is_supported(self):
        from core.authorization.constants import (
            RESPONSIBILITY_BENEFICIARY_REGISTRATION,
        )

        self.assertEqual(
            self.service.get_required_responsibility("beneficiaries"),
            RESPONSIBILITY_BENEFICIARY_REGISTRATION,
        )

    def test_resource_name_is_case_insensitive(self):
        from core.authorization.constants import (
            RESPONSIBILITY_PROJECT_COORDINATION,
        )

        self.assertEqual(
            self.service.get_required_responsibility("PROJECT"),
            RESPONSIBILITY_PROJECT_COORDINATION,
        )

    def test_unknown_resource_has_no_requirement(self):
        self.assertIsNone(
            self.service.get_required_responsibility(
                "unknown_resource"
            )
        )

    def test_empty_resource_has_no_requirement(self):
        self.assertIsNone(
            self.service.get_required_responsibility("")
        )

    def test_none_resource_has_no_requirement(self):
        self.assertIsNone(
            self.service.get_required_responsibility(None)
        )

class AuthorizationServiceIntegrationTests(SimpleTestCase):
    """
    Step 13.11 tests: permission + responsibility integration.

    Resource-level authorization must require both:
        1. the required title permission
        2. the required active responsibility assignment
    """

    def setUp(self):
        self.service = AuthorizationService()

    def make_user(
        self,
        *,
        authenticated=True,
        active=True,
        title_name="Programme Coordinator",
        title_active=True,
        permissions=None,
        responsibilities=None,
    ):
        permission_codes = set(permissions or [])
        responsibility_codes = set(responsibilities or [])

        title_permissions = Mock()

        def permission_filter(**kwargs):
            permission_code = kwargs.get(
                "permission__permission_code"
            )
            result = Mock()
            result.exists.return_value = (
                permission_code in permission_codes
            )
            return result

        title_permissions.filter.side_effect = permission_filter

        title = SimpleNamespace(
            title_name=title_name,
            is_active=title_active,
            title_permissions=title_permissions,
        )

        responsibility_assignments = Mock()

        def responsibility_filter(**kwargs):
            responsibility_code = kwargs.get(
                "responsibility__responsibility_code"
            )
            is_active = kwargs.get("is_active")

            result = Mock()
            result.exists.return_value = (
                responsibility_code in responsibility_codes
                and is_active is True
            )
            return result

        responsibility_assignments.filter.side_effect = (
            responsibility_filter
        )

        return SimpleNamespace(
            is_authenticated=authenticated,
            is_active=active,
            title=title,
            responsibility_assignments=responsibility_assignments,
        )

    def test_permission_and_responsibility_are_required(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertTrue(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_permission_without_responsibility_is_denied(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_responsibility_without_permission_is_denied(self):
        user = self.make_user(
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_inactive_responsibility_assignment_is_denied(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities=set(),
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_wrong_responsibility_is_denied(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_FINANCIAL_OPERATIONS,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_unmapped_resource_is_denied(self):
        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_access_resource(
                user,
                permission=PERMISSION_VIEW,
                resource="unknown_resource",
            )
        )

    def test_unauthenticated_user_is_denied(self):
        user = self.make_user(
            authenticated=False,
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_inactive_user_is_denied(self):
        user = self.make_user(
            active=False,
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_inactive_title_is_denied(self):
        user = self.make_user(
            title_active=False,
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_resource_aware_edit_requires_permission_and_responsibility(self):
        user = self.make_user(
            permissions={PERMISSION_ADD},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertFalse(
            self.service.can_edit(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )

    def test_resource_aware_approve_requires_permission_and_responsibility(self):
        user = self.make_user(
            permissions={PERMISSION_APPROVE},
            responsibilities={
                RESPONSIBILITY_BENEFICIARY_REGISTRATION,
            },
        )

        self.assertTrue(
            self.service.can_approve(
                user,
                record=SimpleNamespace(),
                resource="beneficiary",
            )
        )


class AuthorizationServiceScopeTests(SimpleTestCase):
    """
    Step 13.12 tests: project/activity scope authorization.

    Tests use mocks/test doubles only. No database records are created.
    """

    def setUp(self):
        self.service = AuthorizationService()

    def make_user(
        self,
        *,
        permissions=None,
        responsibilities=None,
        project_assignments=None,
        activity_assignments=None,
    ):
        permission_codes = set(permissions or [])
        responsibility_codes = set(responsibilities or [])
        assigned_projects = list(project_assignments or [])
        assigned_activities = list(activity_assignments or [])

        title_permissions = Mock()
        title_permissions.filter.side_effect = lambda **kwargs: (
            SimpleNamespace(
                exists=lambda: kwargs.get(
                    "permission__permission_code"
                ) in permission_codes
            )
        )

        responsibility_manager = Mock()
        responsibility_manager.filter.side_effect = (
            lambda **kwargs: SimpleNamespace(
                exists=lambda: (
                    kwargs.get(
                        "responsibility__responsibility_code"
                    ) in responsibility_codes
                    and kwargs.get("is_active") is True
                )
            )
        )

        project_manager = Mock()
        project_manager.filter.side_effect = (
            lambda **kwargs: SimpleNamespace(
                exists=lambda: (
                    kwargs.get("project") in assigned_projects
                    and kwargs.get("is_active") is True
                )
            )
        )

        activity_manager = Mock()
        activity_manager.filter.side_effect = (
            lambda **kwargs: SimpleNamespace(
                exists=lambda: (
                    kwargs.get("activity") in assigned_activities
                    and kwargs.get("status") == "assigned"
                )
            )
        )

        title = SimpleNamespace(
            title_name="Programme Coordinator",
            is_active=True,
            title_permissions=title_permissions,
        )

        return SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            title=title,
            responsibility_assignments=responsibility_manager,
            project_assignments=project_manager,
            activity_assignments=activity_manager,
        )

    def make_project(self, project_id):
        return SimpleNamespace(project_id=project_id)

    def make_activity(self, activity_id, project):
        return SimpleNamespace(
            activity_id=activity_id,
            project=project,
        )

    def test_project_scope_requires_active_project_assignment(self):
        project = self.make_project(1)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
            project_assignments=[project],
        )

        self.assertTrue(
            self.service.has_project_scope(user, project)
        )

    def test_project_without_assignment_is_denied(self):
        project = self.make_project(1)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
        )

        self.assertFalse(
            self.service.has_project_scope(user, project)
        )

    def test_different_project_assignment_does_not_grant_scope(self):
        project_one = self.make_project(1)
        project_two = self.make_project(2)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
            project_assignments=[project_one],
        )

        self.assertFalse(
            self.service.has_project_scope(user, project_two)
        )

    def test_project_resource_requires_scope_in_addition_to_permission_and_responsibility(self):
        project = self.make_project(1)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
        )

        self.assertFalse(
            self.service.can_view(
                user,
                project,
                resource="project",
                context={"project": project},
            )
        )

    def test_project_resource_is_allowed_with_permission_responsibility_and_scope(self):
        project = self.make_project(1)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_COORDINATION,
            },
            project_assignments=[project],
        )

        self.assertTrue(
            self.service.can_view(
                user,
                project,
                resource="project",
                context={"project": project},
            )
        )

    def test_activity_scope_requires_parent_project_scope(self):
        project = self.make_project(1)
        activity = self.make_activity(10, project)

        user = self.make_user(
            project_assignments=set(),
            activity_assignments=[activity],
        )

        self.assertFalse(
            self.service.has_activity_scope(user, activity)
        )

    def test_activity_scope_requires_active_activity_assignment(self):
        project = self.make_project(1)
        activity = self.make_activity(10, project)

        user = self.make_user(
            project_assignments=[project],
            activity_assignments=set(),
        )

        self.assertFalse(
            self.service.has_activity_scope(user, activity)
        )

    def test_activity_assignment_to_different_activity_does_not_grant_scope(self):
        project = self.make_project(1)
        activity_one = self.make_activity(10, project)
        activity_two = self.make_activity(20, project)

        user = self.make_user(
            project_assignments=[project],
            activity_assignments=[activity_one],
        )

        self.assertFalse(
            self.service.has_activity_scope(user, activity_two)
        )

    def test_activity_resource_requires_project_and_activity_scope(self):
        project = self.make_project(1)
        activity = self.make_activity(10, project)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_ACTIVITIES,
            },
            project_assignments=[project],
        )

        self.assertFalse(
            self.service.can_view(
                user,
                activity,
                resource="activity",
                context={"activity": activity},
            )
        )

    def test_activity_resource_is_allowed_with_all_required_layers(self):
        project = self.make_project(1)
        activity = self.make_activity(10, project)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_ACTIVITIES,
            },
            project_assignments=[project],
            activity_assignments=[activity],
        )

        self.assertTrue(
            self.service.can_view(
                user,
                activity,
                resource="activity",
                context={"activity": activity},
            )
        )

    def test_activity_cannot_bypass_parent_project_scope(self):
        project = self.make_project(1)
        activity = self.make_activity(10, project)

        user = self.make_user(
            permissions={PERMISSION_VIEW},
            responsibilities={
                RESPONSIBILITY_PROJECT_ACTIVITIES,
            },
            activity_assignments=[activity],
        )

        self.assertFalse(
            self.service.can_view(
                user,
                activity,
                resource="activity",
                context={"activity": activity},
            )
        )
