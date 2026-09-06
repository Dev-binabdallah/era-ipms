from django.contrib.auth.hashers import check_password
from django.db.models import Q

from core.models import Users


class UsersAuthenticationBackend:
    """
    Authenticate ERA-IPMS users using the existing users table.

    Users may authenticate with either their username or email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        identifier = username.strip()

        if not identifier:
            return None

        try:
            user = (
                Users.objects
                .select_related("title")
                .get(
                    Q(username=identifier) | Q(email__iexact=identifier)
                )
            )
        except Users.DoesNotExist:
            return None
        except Users.MultipleObjectsReturned:
            return None

        if not user.is_active:
            return None

        if not check_password(password, user.password_hash):
            return None

        return user

    def get_user(self, user_id):
        try:
            return (
                Users.objects
                .select_related("title")
                .get(pk=user_id)
            )
        except Users.DoesNotExist:
            return None
