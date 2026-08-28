"""Resolution de configuration : DB d'abord, env en fallback.

Les services de la plateforme (LLM, email) utilisent get_setting()
au lieu de lire directement os.environ. Si une valeur est definie en
base (PlatformSetting), elle est utilisee ; sinon on retombe sur la
variable d'environnement. Les secrets non renseignes en base restent
donc lisibles via l'environnement.
"""

from django.conf import settings as django_settings

_SECRET_FIELDS = frozenset(
    {"llm_api_key", "email_host_password", "imap_password"}
)


def get_setting(field_name, env_name=None, default=None):
    """Retourne la valeur DB si non vide, sinon la valeur env/defaut."""
    from .models import PlatformSetting

    obj = PlatformSetting.get_solo()
    value = getattr(obj, field_name, "")
    if value:
        return value
    if env_name:
        import os

        env_value = os.environ.get(env_name, default)
        return env_value if env_value is not None else default
    return default


def get_llm_config():
    return {
        "api_key": get_setting("llm_api_key", "LLM_API_KEY", "missing"),
        "base_url": get_setting(
            "llm_api_base_url", "LLM_API_BASE_URL", "https://api.openai.com/v1"
        ),
        "model": get_setting("llm_model", "LLM_MODEL", "gpt-4o"),
    }


def get_smtp_config():
    return {
        "host": get_setting("email_host", "EMAIL_HOST", ""),
        "port": int(get_setting("email_port", "EMAIL_PORT", "587")),
        "user": get_setting("email_host_user", "EMAIL_HOST_USER", ""),
        "password": get_setting("email_host_password", "EMAIL_HOST_PASSWORD", ""),
        "use_tls": str(
            get_setting("email_use_tls", "EMAIL_USE_TLS", "true")
        ).lower()
        in ("true", "1", "yes", "on"),
        "from_email": get_setting("email_from", "EMAIL_FROM", ""),
    }


def get_imap_config():
    return {
        "host": get_setting("imap_host", "EMAIL_IMAP_HOST", ""),
        "port": int(get_setting("imap_port", "EMAIL_IMAP_PORT", "993")),
        "user": get_setting("imap_user", "EMAIL_IMAP_USER", ""),
        "password": get_setting("imap_password", "EMAIL_IMAP_PASSWORD", ""),
    }


def apply_settings_to_django():
    """Patch settings dynamiquement (SMTP) avec les valeurs DB non vides.

    A appeler dans AppConfig.ready(). django.core.mail lit ces valeurs
    au moment de l'envoi, donc les changements prennent effet sans
    redemarrer le worker (relu a chaque send_mail). Quand un hote SMTP
    est configure, on bascule aussi le backend de 'console' vers un
    vrai envoi SMTP.
    """
    smtp = get_smtp_config()
    if smtp["host"]:
        django_settings.EMAIL_BACKEND = (
            "django.core.mail.backends.smtp.EmailBackend"
        )
        django_settings.EMAIL_HOST = smtp["host"]
        django_settings.EMAIL_PORT = smtp["port"]
        django_settings.EMAIL_HOST_USER = smtp["user"]
        django_settings.EMAIL_HOST_PASSWORD = smtp["password"]
        django_settings.EMAIL_USE_TLS = smtp["use_tls"]
    if smtp["from_email"]:
        django_settings.EMAIL_FROM = smtp["from_email"]

    return smtp


def is_secret_field(name):
    return name in _SECRET_FIELDS
