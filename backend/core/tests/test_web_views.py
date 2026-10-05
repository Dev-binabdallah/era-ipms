from types import SimpleNamespace

from django.test import RequestFactory, SimpleTestCase

from core.web_views import dashboard_page, login_page


class LoginPageTests(SimpleTestCase):
    def test_login_page_loads(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ERA-IPMS")
        self.assertContains(response, "Username or email")
        self.assertContains(response, "Password")
        self.assertContains(response, "Sign in")
        self.assertNotContains(response, "Welcome back")
        self.assertNotContains(
            response,
            "Sign in to access your ERA-IPMS workspace.",
        )
        self.assertContains(response, 'id="login-form"')
        self.assertContains(response, "core/js/login.js")


class DashboardPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_dashboard_redirects_unauthenticated_user(self):
        request = self.factory.get("/dashboard/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = dashboard_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_dashboard_loads_for_authenticated_user(self):
        request = self.factory.get("/dashboard/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = dashboard_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Projects")
        self.assertContains(response, "Activity status")
        self.assertContains(response, "Financial summary")
        self.assertContains(response, "core/js/dashboard.js")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "csrfmiddlewaretoken")
