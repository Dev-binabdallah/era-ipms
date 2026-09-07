import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from core.views import auth_login, auth_logout, auth_me


class AuthenticationApiTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch("core.views.authenticate")
    @patch("core.views.login")
    def test_login_success(self, mock_login, mock_authenticate):
        user = SimpleNamespace(
            user_id=1,
            username="testuser",
            title=SimpleNamespace(title_name="Administrator"),
        )

        mock_authenticate.return_value = user

        request = self.factory.post(
            "/auth/login/",
            {
                "identifier": "testuser",
                "password": "secret",
            },
        )

        response = auth_login(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": True,
                "user_id": 1,
                "username": "testuser",
                "title": "Administrator",
            },
        )

        mock_authenticate.assert_called_once()
        mock_login.assert_called_once()

    @patch("core.views.authenticate")
    def test_login_invalid_credentials(self, mock_authenticate):
        mock_authenticate.return_value = None

        request = self.factory.post(
            "/auth/login/",
            {
                "identifier": "testuser",
                "password": "wrong",
            },
        )

        response = auth_login(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": False,
                "error": "Invalid credentials",
            },
        )

    def test_login_missing_credentials(self):
        request = self.factory.post(
            "/auth/login/",
            {
                "identifier": "",
                "password": "",
            },
        )

        response = auth_login(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": False,
                "error": "Identifier and password are required",
            },
        )

    def test_login_get_not_allowed(self):
        request = self.factory.get("/auth/login/")

        response = auth_login(request)

        self.assertEqual(response.status_code, 405)

    def test_me_anonymous(self):
        request = self.factory.get("/auth/me/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = auth_me(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": False,
            },
        )

    def test_me_authenticated(self):
        user = SimpleNamespace(
            user_id=1,
            username="testuser",
            title=SimpleNamespace(title_name="Administrator"),
            is_authenticated=True,
        )

        request = self.factory.get("/auth/me/")
        request.user = user

        response = auth_me(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": True,
                "user_id": 1,
                "username": "testuser",
                "title": "Administrator",
            },
        )

    @patch("core.views.logout")
    def test_logout(self, mock_logout):
        request = self.factory.post("/auth/logout/")

        response = auth_logout(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "authenticated": False,
                "message": "Logged out successfully",
            },
        )

        mock_logout.assert_called_once_with(request)

    def test_logout_get_not_allowed(self):
        request = self.factory.get("/auth/logout/")

        response = auth_logout(request)

        self.assertEqual(response.status_code, 405)