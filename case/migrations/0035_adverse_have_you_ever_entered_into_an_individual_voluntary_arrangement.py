# Generated by Django 5.1.2 on 2025-03-07 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0034_ccj"),
    ]

    operations = [
        migrations.AddField(
            model_name="adverse",
            name="have_you_ever_entered_into_an_individual_voluntary_arrangement",
            field=models.BooleanField(default=False),
        ),
    ]
