import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import PlatformSetting


class SettingsPermissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/admin/settings/"

    def _auth(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken

        return f"Bearer {RefreshToken.for_user(user).access_token}"

    def test_non_authenticated_forbidden(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_non_staff_forbidden(self):
        user = User.objects.create_user("user", "user@example.com", "Pass1234!")
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=self._auth(user)
        )
        self.assertEqual(response.status_code, 403)

    def test_staff_allowed(self):
        user = User.objects.create_user("admin", "admin@example.com", "Pass1234!")
        user.is_staff = True
        user.save()
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=self._auth(user)
        )
        self.assertEqual(response.status_code, 200)


class SettingsCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/admin/settings/"
        self.admin = User.objects.create_user("admin", "admin@example.com", "Pass1234!")
        self.admin.is_staff = True
        self.admin.save()

        from rest_framework_simplejwt.tokens import RefreshToken

        self.auth = f"Bearer {RefreshToken.for_user(self.admin).access_token}"

    def _get(self):
        return self.client.get(self.url, HTTP_AUTHORIZATION=self.auth)

    def test_get_returns_masked_secrets(self):
        obj = PlatformSetting.get_solo()
        obj.llm_api_key = "secret-key-123"
        obj.save()
        data = self._get().json()
        self.assertTrue(data["llm_api_key_is_set"])
        self.assertNotIn("secret-key-123", data["llm_api_key"])
        self.assertNotEqual(data["llm_api_key"], "secret-key-123")

    def test_put_updates_plain_fields(self):
        response = self.client.put(
            self.url,
            data=json.dumps({"llm_model": "gpt-4o-mini", "email_port": 465}),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.auth,
        )
        self.assertEqual(response.status_code, 200)
        obj = PlatformSetting.get_solo()
        self.assertEqual(obj.llm_model, "gpt-4o-mini")
        self.assertEqual(obj.email_port, 465)

    def test_put_keeps_secret_when_masked(self):
        obj = PlatformSetting.get_solo()
        obj.llm_api_key = "actual-secret"
        obj.save()
        response = self.client.put(
            self.url,
            data=json.dumps({"llm_api_key": "••••••••"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.auth,
        )
        self.assertEqual(response.status_code, 200)
        obj.refresh_from_db()
        self.assertEqual(obj.llm_api_key, "actual-secret")

    def test_put_keeps_secret_when_empty(self):
        obj = PlatformSetting.get_solo()
        obj.imap_password = "actual-password"
        obj.save()
        response = self.client.put(
            self.url,
            data=json.dumps({"imap_password": ""}),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.auth,
        )
        obj.refresh_from_db()
        self.assertEqual(obj.imap_password, "actual-password")

    def test_put_overwrites_secret_when_new_value(self):
        obj = PlatformSetting.get_solo()
        obj.llm_api_key = "old-secret"
        obj.save()
        response = self.client.put(
            self.url,
            data=json.dumps({"llm_api_key": "new-secret-xyz"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.auth,
        )
        obj.refresh_from_db()
        self.assertEqual(obj.llm_api_key, "new-secret-xyz")


class SettingsConfigTest(TestCase):
    def test_env_fallback_when_db_blank(self):
        from settings_app.config import get_setting

        PlatformSetting.get_solo()
        # DB vide -> on simule un env defini
        import os

        os.environ["TEST_FAKE_LLM_KEY"] = "env-key"
        value = get_setting("llm_api_key", "TEST_FAKE_LLM_KEY", "default")
        self.assertEqual(value, "env-key")
        del os.environ["TEST_FAKE_LLM_KEY"]

    def test_db_overrides_env(self):
        from settings_app.config import get_llm_config

        obj = PlatformSetting.get_solo()
        obj.llm_api_key = "db-key-value"
        obj.save()

        import os

        os.environ["LLM_API_KEY"] = "env-key-value"
        cfg = get_llm_config()
        self.assertEqual(cfg["api_key"], "db-key-value")
        del os.environ["LLM_API_KEY"]
