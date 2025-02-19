# Generated by Django 5.1.2 on 2025-02-19 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0017_alter_applicantdetails_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="applicantdetails",
            name="company",
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="applicant_details",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company",
                to="case.applicantdetails",
            ),
            preserve_default=False,
        ),
    ]
