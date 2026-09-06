from core.authorization.constants import (
    PERMISSION_ADD,
    PERMISSION_ADMINISTER,
    PERMISSION_APPROVE,
    PERMISSION_DELETE,
    PERMISSION_EDIT,
    PERMISSION_EXPORT,
    PERMISSION_MANAGE,
    PERMISSION_VIEW,
    RESPONSIBILITIES,
)
from core.authorization.policy import (
    RESOURCE_RESPONSIBILITY_MAP,
    TITLE_RESPONSIBILITY_ELIGIBILITY,
)


class AuthorizationService:
    """
    Central authorization service for ERA-IPMS.

    Authorization layers:

        authentication
            -> active user
            -> active title
            -> title permission
            -> resource responsibility
            -> active responsibility assignment
            -> project/activity scope

    Record-level rules will be added in a subsequent authorization layer.
    """

    def can_view(self, user, record, resource=None, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_VIEW,
            record=record,
            resource=resource,
            context=context,
        )

    def can_add(self, user, resource, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_ADD,
            resource=resource,
            context=context,
        )

    def can_edit(self, user, record, resource=None, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_EDIT,
            record=record,
            resource=resource,
            context=context,
        )

    def can_delete(self, user, record, resource=None, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_DELETE,
            record=record,
            resource=resource,
            context=context,
        )

    def can_approve(self, user, record, resource=None, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_APPROVE,
            record=record,
            resource=resource,
            context=context,
        )

    def can_export(self, user, resource, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_EXPORT,
            resource=resource,
            context=context,
        )

    def can_manage(self, user, resource, context=None):
        return self._check(
            user=user,
            permission=PERMISSION_MANAGE,
            resource=resource,
            context=context,
        )

    def can_administer(self, user):
        return self._check(
            user=user,
            permission=PERMISSION_ADMINISTER,
        )

    def has_permission(self, user, permission):
        """
        Determine whether an active authenticated user has a permission
        through the user's active title.

        This method checks only the title/permission layer.
        It does not grant responsibility or record-level access.
        """

        if not self._is_authenticated(user):
            return False

        if not getattr(user, "is_active", False):
            return False

        title = getattr(user, "title", None)

        if title is None:
            return False

        if not getattr(title, "is_active", False):
            return False

        if not permission:
            return False

        return title.title_permissions.filter(
            permission__permission_code=permission
        ).exists()

    def has_responsibility(self, user, responsibility):
        """
        Determine whether an active user has an active responsibility
        assignment that is eligible for the user's active title.

        Responsibility does not grant a permission by itself.
        """

        if not self._is_authenticated(user):
            return False

        if not getattr(user, "is_active", False):
            return False

        title = getattr(user, "title", None)

        if title is None:
            return False

        if not getattr(title, "is_active", False):
            return False

        if responsibility not in RESPONSIBILITIES:
            return False

        eligible_responsibilities = TITLE_RESPONSIBILITY_ELIGIBILITY.get(
            title.title_name,
            set(),
        )

        if responsibility not in eligible_responsibilities:
            return False

        assignments = getattr(
            user,
            "responsibility_assignments",
            None,
        )

        if assignments is None:
            return False

        return assignments.filter(
            responsibility__responsibility_code=responsibility,
            is_active=True,
        ).exists()

    def get_required_responsibility(self, resource):
        """
        Return the responsibility required for a resource.

        Resource names are normalized to lowercase strings.
        """

        if resource is None:
            return None

        resource_name = str(resource).strip().lower()

        if not resource_name:
            return None

        return RESOURCE_RESPONSIBILITY_MAP.get(resource_name)

    def has_project_scope(self, user, project):
        """
        Determine whether an active user is actively assigned to a project.
        """

        if project is None:
            return False

        assignments = getattr(user, "project_assignments", None)

        if assignments is None:
            return False

        return assignments.filter(
            project=project,
            is_active=True,
        ).exists()

    def has_activity_scope(self, user, activity):
        """
        Determine whether an active user is assigned to an activity and
        also has active scope over the activity's parent project.

        Activity assignments use status='assigned' as the active state.
        """

        if activity is None:
            return False

        project = getattr(activity, "project", None)

        if project is None:
            return False

        if not self.has_project_scope(user, project):
            return False

        assignments = getattr(user, "activity_assignments", None)

        if assignments is None:
            return False

        return assignments.filter(
            activity=activity,
            status="assigned",
        ).exists()

    def has_scope(self, user, resource, record=None, context=None):
        """
        Determine record-level project/activity scope.

        Scope is resolved only through explicitly approved domain
        relationships. Resources without an applicable project/activity
        relationship pass this scope layer. Unknown resources are denied.
        """

        resource_name = str(resource).strip().lower() if resource else ""
        context = context or {}

        if resource_name in {"project", "projects"}:
            project = context.get("project", record)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {"activity", "activities"}:
            activity = context.get("activity", record)

            if activity is None:
                return False

            return self.has_activity_scope(user, activity)

        if resource_name in {
            "activity_participant",
            "activity_participants",
        }:
            activity = getattr(record, "activity", None)

            if activity is None:
                return False

            project = getattr(activity, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "poultry_group",
            "poultry_groups",
        }:
            project = getattr(record, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "poultry_stock_movement",
            "poultry_stock_movements",
            "egg_production",
            "feed_record",
            "feed_records",
            "poultry_health_record",
            "poultry_health_records",
            "poultry_sale",
            "poultry_sales",
        }:
            poultry_group = getattr(record, "poultry_group", None)

            if poultry_group is None:
                return False

            project = getattr(poultry_group, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "farm",
            "farms",
            "farm_crop",
            "farm_crops",
        }:
            project = getattr(record, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "farm_activity",
            "farm_activities",
        }:
            crop = getattr(record, "crop", None)

            if crop is None:
                return False

            project = getattr(crop, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "harvest",
            "harvests",
        }:
            crop = getattr(record, "crop", None)

            if crop is None:
                return False

            project = getattr(crop, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "farm_poultry_transfer",
            "farm_poultry_transfers",
        }:
            harvest = getattr(record, "harvest", None)
            poultry_group = getattr(record, "poultry_group", None)

            if harvest is None or poultry_group is None:
                return False

            crop = getattr(harvest, "crop", None)
            farm_project = getattr(crop, "project", None) if crop else None
            poultry_project = getattr(poultry_group, "project", None)

            if farm_project is None or poultry_project is None:
                return False

            if farm_project != poultry_project:
                return False

            return self.has_project_scope(user, farm_project)

        if resource_name in {
            "financial_transaction",
            "financial_transactions",
        }:
            project = getattr(record, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "me_indicator",
            "me_indicators",
        }:
            project = getattr(record, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "me_indicator_record",
            "me_indicator_records",
        }:
            indicator = getattr(record, "indicator", None)

            if indicator is None:
                return False

            project = getattr(indicator, "project", None)

            if project is None:
                return False

            return self.has_project_scope(user, project)

        if resource_name in {
            "beneficiary",
            "beneficiaries",
            "disability_assessment",
            "disability_assessments",
            "home_visit",
            "home_visits",
            "referral",
            "referrals",
            "follow_up",
            "follow_ups",
            "referral_follow_up",
            "referral_follow_ups",
            "disability_service",
            "disability_services",
            "community_awareness",
        }:
            return True

        return False

    def can_access_resource(
        self,
        user,
        *,
        permission,
        resource,
        record=None,
        context=None,
    ):
        """
        Evaluate permission, responsibility, and applicable scope.
        """

        if not self.has_permission(user, permission):
            return False

        required_responsibility = (
            self.get_required_responsibility(resource)
        )

        if required_responsibility is None:
            return False

        if not self.has_responsibility(
            user,
            required_responsibility,
        ):
            return False

        return self.has_scope(
            user,
            resource,
            record=record,
            context=context,
        )

    def _check(
        self,
        *,
        user,
        permission,
        record=None,
        resource=None,
        context=None,
    ):
        """
        Central authorization decision point.

        Resource-aware calls require permission, responsibility, and
        applicable project/activity scope.

        If no resource is supplied, only the permission layer is checked.
        """

        if resource is None:
            return self.has_permission(user, permission)

        return self.can_access_resource(
            user,
            permission=permission,
            resource=resource,
            record=record,
            context=context,
        )

    @staticmethod
    def _is_authenticated(user):
        if user is None:
            return False

        return bool(getattr(user, "is_authenticated", False))


authorization_service = AuthorizationService()
