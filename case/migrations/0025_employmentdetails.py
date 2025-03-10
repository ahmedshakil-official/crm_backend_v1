# Generated by Django 5.1.2 on 2025-02-24 09:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0024_applicantdetails_is_dual_nationality_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EmploymentDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "alias",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_ip",
                    models.GenericIPAddressField(blank=True, editable=False, null=True),
                ),
                (
                    "employment_status",
                    models.CharField(
                        choices=[
                            ("EMPLOYED", "Employed"),
                            ("SELF_EMPLOYED", "Self Employed"),
                            ("RETIRED", "Retired"),
                            ("OTHER", "Other"),
                            ("UNEMPLOYED", "Unemployed"),
                            ("HOUSEPERSON", "Houseperson"),
                            ("CONTRACTOR", "Contractor"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "employment_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PERMANENT", "Permanent"),
                            ("CONTRACT", "Contract"),
                            ("TEMPORARY", "Temporary"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("occupation", models.CharField(blank=True, max_length=255, null=True)),
                ("industry", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "employer_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_telephone",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_email_for_reference",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "employer_postcode",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "employer_house_name_or_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_address_line_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_address_line_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_city",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_county",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "employer_country",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("employment_commenced", models.DateField(blank=True, null=True)),
                ("employment_ended", models.DateField(blank=True, null=True)),
                (
                    "gross_annual_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "net_annual_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("is_probationary_period", models.BooleanField(default=False)),
                ("is_income_in_foreign_currency", models.BooleanField(default=False)),
                (
                    "bonus",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("is_bonus_guaranteed", models.BooleanField(default=False)),
                (
                    "bonus_frequency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NEVER", "Never"),
                            ("DAILY", "Daily"),
                            ("WEEKLY", "Weekly"),
                            ("BI_WEEKLY", "Bi Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("BI_MONTHLY", "Bi Monthly"),
                            ("QUARTERLY", "Quarterly"),
                            ("BI_ANNUALLY", "Bi Annually"),
                            ("ANNUALLY", "Annually"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "overtime",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("is_overtime_guaranteed", models.BooleanField(default=False)),
                (
                    "overtime_frequency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NEVER", "Never"),
                            ("DAILY", "Daily"),
                            ("WEEKLY", "Weekly"),
                            ("BI_WEEKLY", "Bi Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("BI_MONTHLY", "Bi Monthly"),
                            ("QUARTERLY", "Quarterly"),
                            ("BI_ANNUALLY", "Bi Annually"),
                            ("ANNUALLY", "Annually"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "allowance",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("is_allowance_guaranteed", models.BooleanField(default=False)),
                (
                    "allowance_frequency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NEVER", "Never"),
                            ("DAILY", "Daily"),
                            ("WEEKLY", "Weekly"),
                            ("BI_WEEKLY", "Bi Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("BI_MONTHLY", "Bi Monthly"),
                            ("QUARTERLY", "Quarterly"),
                            ("BI_ANNUALLY", "Bi Annually"),
                            ("ANNUALLY", "Annually"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "business_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_telephone",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_house_name_or_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_postcode",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "business_address_line_1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_address_line_2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_city",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_county",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "business_country",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("job_title", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "company_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PRIVATE_LIMITED", "Private Limited Company"),
                            ("PUBLIC_LIMITED", "Public Limited Company"),
                            ("SOLE_TRADER", "Sole Trader"),
                            ("PARTNERSHIP", "Partnership"),
                            (
                                "LIMITED_LIABILITY_PARTNERSHIP",
                                "Limited Liability Partnership",
                            ),
                            ("OTHER", "Other"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "percentage_of_business_owned",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("is_accounts_available", models.BooleanField(default=False)),
                (
                    "year1",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="e.g. 2014", null=True
                    ),
                ),
                (
                    "year1_net_profit",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Net profit for Year 1 (default is 0 if not provided)",
                    ),
                ),
                (
                    "year2",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="e.g. 2013", null=True
                    ),
                ),
                (
                    "year2_net_profit",
                    models.PositiveIntegerField(
                        default=0, help_text="Net profit for Year 2"
                    ),
                ),
                (
                    "year3",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="e.g. 2012", null=True
                    ),
                ),
                (
                    "year3_net_profit",
                    models.PositiveIntegerField(
                        default=0, help_text="Net profit for Year 3"
                    ),
                ),
                (
                    "accountant_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "accountant_qualifications",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "salary",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "dividends",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "turnover",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("further_details", models.TextField(blank=True, null=True)),
                (
                    "income_source",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "other_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "other_income_source",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("other_income_start_date", models.DateField(blank=True, null=True)),
                (
                    "contractor_industry",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("current_contract_start", models.DateField(blank=True, null=True)),
                ("current_contract_end", models.DateField(blank=True, null=True)),
                (
                    "time_contracting",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "day_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employment_details",
                        to="case.case",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s_set",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s_set",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employment_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("case", "user")},
            },
        ),
    ]
