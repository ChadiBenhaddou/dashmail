from django.apps import AppConfig


class SettingsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "settings_app"
    verbose_name = "Configuration plateforme"

    def ready(self):
        from django.apps import apps

        try:
            if apps.ready and apps.get_model("settings_app", "PlatformSetting").objects.exists():
                from .config import apply_settings_to_django

                apply_settings_to_django()
        except Exception:
            # La base peut ne pas etre prete (migrations initiales).
            pass
