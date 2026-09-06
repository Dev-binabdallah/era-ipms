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
        Determine project/activity scope for resources that require it.

        Project resources require an active project assignment.

        Activity resources require:
            1. an active project assignment for the activity's project
            2. an active activity assignment

        Scope is intentionally explicit through record/context so that
        authorization does not guess relationships between unrelated
        records.
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

        return True

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
