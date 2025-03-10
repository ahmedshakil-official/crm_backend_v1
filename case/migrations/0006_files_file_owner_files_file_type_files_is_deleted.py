# Generated by Django 5.1.2 on 2024-12-11 15:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0005_jointuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="files",
            name="file_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="files",
            name="file_type",
            field=models.CharField(
                choices=[
                    ("COMPLIANCE_DOCUMENTS", "Compliance Documents"),
                    ("FACT_FINDS", "Fact Finds"),
                    ("IDS", "IDs"),
                    ("PROOF_OF_ADDRESS", "Proof of Address"),
                    ("INCOME_DOCUMENTS", "Income Documents"),
                    ("BANK_STATEMENTS", "Bank Statements"),
                    (
                        "PROOF_OF_DEPOSIT_BANK_STATEMENTS",
                        "Proof of Deposit - Bank Statements",
                    ),
                    ("DONOR_DOCUMENTS", "Donor Documents"),
                    ("CREDIT_REPORT", "Credit Report"),
                    ("RESEARCH_DOCUMENTS", "Research Documents"),
                    ("LENDERS_KFI", "Lender's KFI"),
                    ("LENDERS_DIP", "Lender's DIP"),
                    (
                        "LENDERS_FULL_MORTGAGE_APPLICATION",
                        "Lender's Full Mortgage Application",
                    ),
                    ("LENDERS_OFFER", "Lender's Offer"),
                    ("SUITABILITY_LETTER", "Suitability Letter"),
                    ("GENERAL_INSURANCE_DOCUMENTS", "General Insurance Documents"),
                    ("PROTECTION_DOCUMENTS", "Protection Documents"),
                    ("AML_AND_SANCTIONS_SEARCH", "AML and Sanctions Search"),
                    ("OTHERS", "Others"),
                ],
                default="IDS",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="files",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
