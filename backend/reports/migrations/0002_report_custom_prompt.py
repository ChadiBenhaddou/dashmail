from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="custom_prompt",
            field=models.TextField(blank=True, default=""),
        ),
    ]
