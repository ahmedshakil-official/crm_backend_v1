# Generated by Django 5.1.2 on 2025-03-10 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0041_notes"),
    ]

    operations = [
        migrations.AddField(
            model_name="existingprotection",
            name="case",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="existing_protection",
                to="case.case",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="notes",
            name="case",
            field=models.ForeignKey(
                default=23,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notes_related",
                to="case.case",
            ),
            preserve_default=False,
        ),
    ]
