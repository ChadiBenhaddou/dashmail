import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlatformSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("llm_api_key", models.TextField(blank=True, default="")),
                ("llm_api_base_url", models.TextField(blank=True, default="")),
                ("llm_model", models.CharField(blank=True, default="", max_length=120)),
                ("email_host", models.CharField(blank=True, default="", max_length=255)),
                ("email_port", models.PositiveIntegerField(default=587)),
                ("email_host_user", models.CharField(blank=True, default="", max_length=255)),
                ("email_host_password", models.TextField(blank=True, default="")),
                ("email_use_tls", models.BooleanField(default=True)),
                ("email_from", models.EmailField(blank=True, default="")),
                ("imap_host", models.CharField(blank=True, default="", max_length=255)),
                ("imap_port", models.PositiveIntegerField(default=993)),
                ("imap_user", models.CharField(blank=True, default="", max_length=255)),
                ("imap_password", models.TextField(blank=True, default="")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Configuration plateforme",
                "verbose_name_plural": "Configuration plateforme",
            },
        ),
    ]
