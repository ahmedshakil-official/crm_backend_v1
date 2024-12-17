# Generated by Django 5.1.2 on 2024-12-17 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0010_alter_organization_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("INTRODUCER", "Introducer"),
                    ("ADVISOR", "Advisor"),
                    ("ADMIN", "Admin"),
                    ("LEAD", "Lead"),
                    ("CLIENT", "Client"),
                    ("JOINT_USER", "Joint User"),
                ],
                default="ADVISOR",
                max_length=64,
                verbose_name="Role",
            ),
        ),
    ]
