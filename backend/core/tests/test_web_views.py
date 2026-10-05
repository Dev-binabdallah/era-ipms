from types import SimpleNamespace

from django.test import RequestFactory, SimpleTestCase

from core.web_views import (
    dashboard_page,
    login_page,
    beneficiaries_page,
    projects_page,
    poultry_page,
    farm_page,
    finance_page,
    me_page,
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
        self.assertContains(response, "Disability assessments")
        self.assertContains(response, "Home visits")
        self.assertContains(response, "Referrals")
        self.assertContains(response, 'id="beneficiary-count"')
        self.assertContains(response, 'id="assessment-count"')
        self.assertContains(response, 'id="home-visit-count"')
        self.assertContains(response, 'id="referral-count"')
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
        self.assertContains(response, "Stock movements")
        self.assertContains(response, "Egg production")
        self.assertContains(response, "Feed records")
        self.assertContains(response, "Health records")
        self.assertContains(response, "Poultry sales")
        self.assertContains(response, 'id="poultry-count"')
        self.assertContains(response, 'id="stock-count"')
        self.assertContains(response, 'id="egg-count"')
        self.assertContains(response, 'id="feed-count"')
        self.assertContains(response, 'id="health-count"')
        self.assertContains(response, 'id="sales-count"')
        self.assertContains(
            response,
            "core/js/poultry.js",
        )
        self.assertContains(
            response,
            "Back to dashboard",
        )


class FarmPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_farm_redirects_unauthenticated_user(self):
        request = self.factory.get("/farm-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = farm_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_farm_page_loads_for_authenticated_user(self):
        request = self.factory.get("/farm-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = farm_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Small Farm Operations")
        self.assertContains(response, "Farm Crops")
        self.assertContains(response, "Farm activities")
        self.assertContains(response, "Harvests")
        self.assertContains(response, "Poultry transfers")
        self.assertContains(response, 'id="farm-count"')
        self.assertContains(response, 'id="activity-count"')
        self.assertContains(response, 'id="harvest-count"')
        self.assertContains(response, 'id="transfer-count"')
        self.assertContains(
            response,
            "core/js/farm.js",
        )
        self.assertContains(
            response,
            "Back to dashboard",
        )


class FinancePageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_finance_redirects_unauthenticated_user(self):
        request = self.factory.get("/finance-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = finance_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_finance_page_loads_for_authenticated_user(self):
        request = self.factory.get("/finance-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = finance_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Financial Operations")
        self.assertContains(response, "Financial Transactions")
        self.assertContains(
            response,
            "core/js/finance.js",
        )
        self.assertContains(
            response,
            "Back to dashboard",
        )

class MePageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_me_redirects_unauthenticated_user(self):
        request = self.factory.get("/me-ui/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = me_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/login/")

    def test_me_page_loads_for_authenticated_user(self):
        request = self.factory.get("/me-ui/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = me_page(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Monitoring & Evaluation")
        self.assertContains(response, "Indicators")
        self.assertContains(response, "Indicator records")
        self.assertContains(response, "me-record-list")
        self.assertContains(response, "core/js/me.js")
        self.assertContains(response, "Back to dashboard")
