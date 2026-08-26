import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "source_file",
                    models.FileField(upload_to="reports/"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("parsing", "Parsing"),
                            ("analyzing", "Analyzing"),
                            ("generating", "Generating"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "dashboard_link",
                    models.UUIDField(default=uuid.uuid4, unique=True),
                ),
                (
                    "row_count",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "column_count",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "file_size",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "llm_insights",
                    models.JSONField(blank=True, null=True),
                ),
                (
                    "charts_config",
                    models.JSONField(blank=True, null=True),
                ),
                (
                    "data_quality_score",
                    models.FloatField(blank=True, null=True),
                ),
                (
                    "cleaning_log",
                    models.JSONField(blank=True, null=True),
                ),
                (
                    "error_message",
                    models.TextField(blank=True, default=""),
                ),
                (
                    "sender_email",
                    models.EmailField(blank=True, default="", max_length=254),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "processed_at",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
            options={
                "verbose_name": "Report",
                "verbose_name_plural": "Reports",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="DataFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "report",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data_file",
                        to="reports.report",
                    ),
                ),
                (
                    "file",
                    models.FileField(upload_to="data_files/"),
                ),
                (
                    "original_filename",
                    models.CharField(max_length=255),
                ),
                (
                    "file_type",
                    models.CharField(max_length=10),
                ),
                (
                    "parsing_status",
                    models.CharField(
                        choices=[
                            ("received", "Received"),
                            ("parsing", "Parsing"),
                            ("parsed", "Parsed"),
                            ("error", "Error"),
                        ],
                        default="received",
                        max_length=20,
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(blank=True, null=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
            ],
            options={
                "verbose_name": "Data File",
                "verbose_name_plural": "Data Files",
            },
        ),
    ]
