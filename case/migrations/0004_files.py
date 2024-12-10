# Generated by Django 5.1.2 on 2024-12-10 15:20

import case.utils
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0003_alter_case_case_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Files",
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
                    "file",
                    models.FileField(
                        help_text="Upload the file",
                        upload_to=case.utils.upload_to_case_files,
                        verbose_name="File",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Optional name of the file",
                        max_length=500,
                        null=True,
                        verbose_name="File Name",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Optional description of the file",
                        max_length=1000,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "special_notes",
                    models.CharField(
                        blank=True,
                        help_text="Optional special notes related to the file",
                        max_length=1000,
                        null=True,
                        verbose_name="Special Notes",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="case.case",
                        verbose_name="Related Case",
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
            ],
            options={
                "verbose_name": "Case File",
                "verbose_name_plural": "Case Files",
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
    ]
