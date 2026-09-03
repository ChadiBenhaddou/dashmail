import json

from django.contrib.auth.models import User
from django.test import Client, TestCase


class AuthRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/auth/register/"

    def test_register_success(self):
        response = self.client.post(
            self.url,
            json.dumps({"username": "testuser", "email": "test@example.com", "password": "TestPass123!", "password_confirm": "TestPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("tokens", data)
        self.assertIn("access", data["tokens"])
        self.assertEqual(data["user"]["email"], "test@example.com")
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_register_duplicate_email(self):
        User.objects.create_user("existing", "test@example.com", "TestPass123!")
        response = self.client.post(
            self.url,
            json.dumps({"username": "newuser", "email": "test@example.com", "password": "TestPass123!", "password_confirm": "TestPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_password_mismatch(self):
        response = self.client.post(
            self.url,
            json.dumps({"username": "testuser", "email": "test@example.com", "password": "TestPass123!", "password_confirm": "Different123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_short_password(self):
        response = self.client.post(
            self.url,
            json.dumps({"username": "testuser", "email": "test@example.com", "password": "short", "password_confirm": "short"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class AuthLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/auth/login/"
        User.objects.create_user("testuser", "test@example.com", "TestPass123!")

    def test_login_success(self):
        response = self.client.post(
            self.url,
            json.dumps({"email": "test@example.com", "password": "TestPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("tokens", data)
        self.assertIn("access", data["tokens"])

    def test_login_wrong_password(self):
        response = self.client.post(
            self.url,
            json.dumps({"email": "test@example.com", "password": "WrongPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_nonexistent_email(self):
        response = self.client.post(
            self.url,
            json.dumps({"email": "nobody@example.com", "password": "TestPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        response = self.client.post(
            self.url,
            json.dumps({"email": "", "password": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class AuthMeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "TestPass123!")

    def test_me_authenticated(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        token = str(RefreshToken.for_user(self.user).access_token)
        response = self.client.get(
            "/api/auth/me/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_me_unauthenticated(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 401)


class AuthRefreshTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "TestPass123!")

    def test_refresh_returns_new_access_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = str(RefreshToken.for_user(self.user))
        response = self.client.post(
            "/api/auth/token/refresh/",
            json.dumps({"refresh": refresh}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
