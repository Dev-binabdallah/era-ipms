from django.test import SimpleTestCase


class LoginPageTests(SimpleTestCase):
    def test_login_page_loads(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ERA-IPMS")
        self.assertContains(response, "Username or email")
        self.assertContains(response, "Password")
        self.assertContains(response, "Sign in")
        self.assertContains(response, 'id="login-form"')
        self.assertContains(response, "core/js/login.js")
