# Generated by Django 5.1.4 on 2024-12-27 15:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0002_auto_20210131_0934"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="action_assignees",
            field=models.ManyToManyField(
                related_name="user_report_actions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Assigned to",
            ),
        ),
    ]
