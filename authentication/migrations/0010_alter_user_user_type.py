# Generated by Django 5.1.2 on 2024-12-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0009_alter_user_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("LEAD", "Lead"),
                    ("CLIENT", "Client"),
                    ("ADVISOR", "Advisor"),
                    ("INTRODUCER", "Introducer"),
                    ("SERVICE_HOLDER", "Service Holder"),
                    ("JOINT_USER", "Joint User"),
                ],
                default="LEAD",
                max_length=20,
            ),
        ),
    ]
