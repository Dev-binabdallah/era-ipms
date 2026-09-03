from django.contrib.auth.hashers import check_password
from core.models import Users


class UsersAuthenticationBackend:
    """
    Authenticate ERA-IPMS users using the existing users table.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = Users.objects.select_related("role").get(
                username=username
            )
        except Users.DoesNotExist:
            return None

        if not user.is_active:
            return None

        if not check_password(password, user.password_hash):
            return None

        return user

    def get_user(self, user_id):
        try:
            return Users.objects.select_related("role").get(
                pk=user_id
            )
        except Users.DoesNotExist:
            return None