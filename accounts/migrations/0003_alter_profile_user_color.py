# Generated by Django 5.1.4 on 2024-12-27 15:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_auto_20210131_0934"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user_color",
            field=models.CharField(default="(239,75,202,.3)", max_length=100),
        ),
    ]
