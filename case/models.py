from django.db import models

from authentication.models import User
from common.models import CreatedAtUpdatedAtBaseModel
from common.enums import ProductCategoryChoices, ApplicantTypeChoices, CaseStageChoices, CaseStatusChoices
from organization.models import Organization



class Case(CreatedAtUpdatedAtBaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    lead = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    product_category = models.CharField(
        max_length=50,
        choices=ProductCategoryChoices.choices,
        default=ProductCategoryChoices.MORTGAGES,
        db_index=True
    )
    applicant_type = models.CharField(
        max_length=50,
        choices=ApplicantTypeChoices.choices,
        default=ApplicantTypeChoices.SINGLE,
        db_index=True
    )
    case_status = models.CharField(
        max_length=50,
        choices=CaseStatusChoices.choices,
        default=CaseStatusChoices.NEW_LEAD,
        db_index=True
    )
    case_stage = models.CharField(
        max_length=50,
        choices=CaseStageChoices.choices,
        default=CaseStageChoices.INQUIRY,
        db_index=True
    )
    notes = models.TextField(blank=True, null=True)
    is_removed = models.BooleanField(default=False, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


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
        # Generate name if not set
        if not self.name:
            self.name = self.generate_case_name()
        super().save(*args, **kwargs)