from types import SimpleNamespace

from django.test import RequestFactory, SimpleTestCase

from core.web_views import (
    dashboard_page,
    login_page,
    beneficiaries_page,
    projects_page,
    poultry_page,
)


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
        self.assertContains(response, 'href="/projects-ui/"')
        self.assertContains(response, "Activity status")
        self.assertContains(response, "Financial summary")
        self.assertContains(response, "core/js/dashboard.js")
        self.assertContains(response, "csrfmiddlewaretoken")


class ProjectsPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_projects_redirects_unauthenticated_user(self):
        request = self.factory.get("/projects-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = projects_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_projects_page_loads_for_authenticated_user(self):
        request = self.factory.get("/projects-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = projects_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects & Activities")
        self.assertContains(response, "Projects")
        self.assertContains(response, "core/js/projects.js")
        self.assertContains(response, "Back to dashboard")


class BeneficiariesPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_beneficiaries_redirects_unauthenticated_user(self):
        request = self.factory.get("/beneficiaries-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = beneficiaries_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_beneficiaries_page_loads_for_authenticated_user(self):
        request = self.factory.get("/beneficiaries-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = beneficiaries_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beneficiary Services")
        self.assertContains(response, "Beneficiaries")
        self.assertContains(
            response,
            "core/js/beneficiaries.js",
        )
        self.assertContains(
            response,
            "Back to dashboard",
        )


class PoultryPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_poultry_redirects_unauthenticated_user(self):
        request = self.factory.get("/poultry-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = poultry_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_poultry_page_loads_for_authenticated_user(self):
        request = self.factory.get("/poultry-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = poultry_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Poultry Operations")
        self.assertContains(response, "Poultry Groups")
        self.assertContains(
            response,
            "core/js/poultry.js",
        )
        self.assertContains(
            response,
            "Back to dashboard",
        )
