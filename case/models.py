from django.db import models

from authentication.models import User
from common.models import CreatedAtUpdatedAtBaseModel
from common.enums import (
    ProductCategoryChoices,
    ApplicantTypeChoices,
    CaseStageChoices,
    CaseStatusChoices,
    FileTypeChoices,
    MeetingTypeChoices,
    MeetingStatusChoices,
)
from organization.models import Organization
from .utils import upload_to_case_files


class Case(CreatedAtUpdatedAtBaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    lead = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    case_category = models.CharField(
        max_length=50,
        choices=ProductCategoryChoices.choices,
        default=ProductCategoryChoices.MORTGAGE,
        db_index=True,
    )
    applicant_type = models.CharField(
        max_length=50,
        choices=ApplicantTypeChoices.choices,
        default=ApplicantTypeChoices.SINGLE,
        db_index=True,
    )
    case_status = models.CharField(
        max_length=50,
        choices=CaseStatusChoices.choices,
        default=CaseStatusChoices.NEW_LEAD,
        db_index=True,
    )
    case_stage = models.CharField(
        max_length=50,
        choices=CaseStageChoices.choices,
        default=CaseStageChoices.INQUIRY,
        db_index=True,
    )
    notes = models.TextField(blank=True, null=True)
    is_removed = models.BooleanField(default=False, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.name

    def generate_case_name(self):
        # Mapping case stage choices to abbreviations
        stage_mapping = {
            "INQUIRY": "INQ",
            "FACT_FIND": "FFD",
            "RESEARCH_COMPLIANCE_CHECK": "RCC",
            "DECISION_IN_PRINCIPLE": "DIP",
            "FULL_MORTGAGE_APPLICATION": "FMA",
            "OFFER_FROM_BANK": "OFB",
            "LEGAL": "LEG",
            "COMPLETION": "COM",
            "FUTURE_OPPORTUNITY": "FOP",
            "NOT_PROCEED": "NPD",
        }
        # Get the 3-letter abbreviation for the case stage
        stage_abbreviation = stage_mapping.get(self.case_stage, "UNK")
        # Use the last 8 characters of the alias
        alias_suffix = str(self.alias).replace("-", "")[-8:]
        return f"{stage_abbreviation}-{alias_suffix}"

    def save(self, *args, **kwargs):
        # Check if the case_stage has changed
        if self.pk:  # Check if the instance already exists (for updates)
            original = Case.objects.get(pk=self.pk)
            if original.case_stage != self.case_stage:
                # If the case_stage is different, regenerate the name
                self.name = self.generate_case_name()
        else:
            # For new cases, generate the name if not set
            if not self.name:
                self.name = self.generate_case_name()

        # Call the parent save method
        super().save(*args, **kwargs)


class Files(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Related Case",
    )
    file = models.FileField(
        upload_to=upload_to_case_files,
        verbose_name="File",
        help_text="Upload the file",
    )
    file_type = models.CharField(
        max_length=50,
        choices=FileTypeChoices.choices,
        default=FileTypeChoices.IDS,
        db_index=True,
    )
    file_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index=True
    )
    is_removed = models.BooleanField(default=False, db_index=True)
    name = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="File Name",
        help_text="Optional name of the file",
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional description of the file",
    )
    special_notes = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Special Notes",
        help_text="Optional special notes related to the file",
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Case File"
        verbose_name_plural = "Case Files"

    def __str__(self):
        return f"{self.case.name} - {self.file.name}"


class JointUser(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="joint_users",
        verbose_name="Related Case",
    )
    joint_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="joint_user_cases",
        verbose_name="Joint User",
    )
    relationship = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Additional notes about the joint user",
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Joint User"
        verbose_name_plural = "Joint Users"

    def __str__(self):
        return f"(Case: {self.case.name}) Joint User: {self.joint_user}"


class Meeting(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="meetings",
        verbose_name="Related Case",
    )
    meeting_type = models.CharField(
        max_length=50,
        choices=MeetingTypeChoices.choices,
        default=MeetingTypeChoices.UPCOMING,
        db_index=True,
    )
    meeting_status = models.CharField(
        max_length=50,
        choices=MeetingStatusChoices.choices,
        default=MeetingStatusChoices.CONFIRMED,
        db_index=True,
    )
    special_notes = models.CharField(max_length=500, null=True, blank=True)
    meeting_link = models.URLField(null=True, blank=True)
    meeting_date = models.DateField(null=True, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)
    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Meeting"

