# Generated by Django 5.1.2 on 2024-11-28 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0007_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("-created_at",)},
        ),
    ]
