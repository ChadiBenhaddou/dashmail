from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0002_report_custom_prompt"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="computed_kpis",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="report",
            name="dashboard_profile",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="report",
            name="kpi_config",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
