# Generated by Django 5.1.2 on 2025-02-26 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0027_alter_employmentdetails_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employmentdetails",
            name="employment_time_month",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="employmentdetails",
            name="employment_time_year",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
