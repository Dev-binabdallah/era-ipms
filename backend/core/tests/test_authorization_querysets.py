from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from core.authorization.constants import PERMISSION_VIEW
from core.authorization.policy import (
    RESPONSIBILITY_BENEFICIARY_REGISTRATION,
    RESPONSIBILITY_FARM_OPERATIONS,
    RESPONSIBILITY_FINANCIAL_OPERATIONS,
    RESPONSIBILITY_MONITORING_EVALUATION,
    RESPONSIBILITY_POULTRY_OPERATIONS,
    RESPONSIBILITY_PROJECT_ACTIVITIES,
    RESPONSIBILITY_PROJECT_COORDINATION,
)
from core.authorization.querysets import authorized_queryset


class AuthorizedQuerysetTests(SimpleTestCase):
    def setUp(self):
        self.user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
        )

        self.queryset = Mock()
        self.filtered_queryset = Mock()

        self.queryset.filter.return_value = self.filtered_queryset
        self.filtered_queryset.distinct.return_value = self.filtered_queryset
        self.queryset.none.return_value = self.filtered_queryset

    def configure_authorization(
        self,
        responsibility=RESPONSIBILITY_PROJECT_COORDINATION,
        permission=True,
    ):
        self.permission = permission
        self.responsibility = responsibility

    def authorization_side_effect(self):
        return self.permission

    def test_unauthenticated_user_gets_none(self):
        self.user.is_authenticated = False

        result = authorized_queryset(
            self.user,
            "project",
            self.queryset,
        )

        self.queryset.none.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    def test_inactive_user_gets_none(self):
        self.user.is_active = False

        result = authorized_queryset(
            self.user,
            "project",
            self.queryset,
        )

        self.queryset.none.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    def test_unknown_resource_gets_none(self):
        result = authorized_queryset(
            self.user,
            "unknown_resource",
            self.queryset,
        )

        self.queryset.none.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_missing_view_permission_gets_none(self, service):
        service.has_permission.return_value = False

        result = authorized_queryset(
            self.user,
            "project",
            self.queryset,
        )

        service.has_permission.assert_called_once_with(
            self.user,
            PERMISSION_VIEW,
        )
        self.queryset.none.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_missing_responsibility_gets_none(self, service):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_PROJECT_COORDINATION
        )
        service.has_responsibility.return_value = False

        result = authorized_queryset(
            self.user,
            "project",
            self.queryset,
        )

        service.has_responsibility.assert_called_once_with(
            self.user,
            RESPONSIBILITY_PROJECT_COORDINATION,
        )
        self.queryset.none.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_project_queryset_requires_active_project_assignment(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_PROJECT_COORDINATION
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "project",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            user_assignments__user=self.user,
            user_assignments__is_active=True,
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_activity_queryset_requires_project_and_activity_assignment(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_PROJECT_ACTIVITIES
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "activity",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            project__user_assignments__user=self.user,
            project__user_assignments__is_active=True,
            assignments__user=self.user,
            assignments__status="assigned",
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_poultry_record_inherits_project_scope(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_POULTRY_OPERATIONS
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "egg_production",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            poultry_group__project__user_assignments__user=self.user,
            poultry_group__project__user_assignments__is_active=True,
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_farm_activity_inherits_crop_project_scope(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_FARM_OPERATIONS
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "farm_activity",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            crop__project__user_assignments__user=self.user,
            crop__project__user_assignments__is_active=True,
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_financial_transaction_requires_project_scope(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_FINANCIAL_OPERATIONS
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "financial_transaction",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            project__user_assignments__user=self.user,
            project__user_assignments__is_active=True,
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_me_indicator_record_inherits_indicator_project_scope(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_MONITORING_EVALUATION
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "me_indicator_record",
            self.queryset,
        )

        self.queryset.filter.assert_called_once_with(
            indicator__project__user_assignments__user=self.user,
            indicator__project__user_assignments__is_active=True,
        )
        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_transfer_requires_matching_farm_and_poultry_project(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_FARM_OPERATIONS
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "farm_poultry_transfer",
            self.queryset,
        )

        self.queryset.filter.assert_called_once()

        filter_kwargs = self.queryset.filter.call_args.kwargs

        self.assertEqual(
            filter_kwargs[
                "harvest__crop__project__user_assignments__user"
            ],
            self.user,
        )
        self.assertTrue(
            filter_kwargs[
                "harvest__crop__project__user_assignments__is_active"
            ]
        )
        self.assertEqual(
            filter_kwargs[
                "poultry_group__project__user_assignments__user"
            ],
            self.user,
        )
        self.assertTrue(
            filter_kwargs[
                "poultry_group__project__user_assignments__is_active"
            ]
        )

        from django.db.models import F

        self.assertEqual(
            filter_kwargs["harvest__crop__project_id"],
            F("poultry_group__project_id"),
        )

        self.filtered_queryset.distinct.assert_called_once_with()
        self.assertIs(result, self.filtered_queryset)

    @patch(
        "core.authorization.querysets.authorization_service"
    )
    def test_beneficiary_resource_is_not_artificially_project_filtered(
        self,
        service,
    ):
        service.has_permission.return_value = True
        service.get_required_responsibility.return_value = (
            RESPONSIBILITY_BENEFICIARY_REGISTRATION
        )
        service.has_responsibility.return_value = True

        result = authorized_queryset(
            self.user,
            "beneficiary",
            self.queryset,
        )

        self.queryset.filter.assert_not_called()
        self.queryset.none.assert_not_called()
        self.assertIs(result, self.queryset)
