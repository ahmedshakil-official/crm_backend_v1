from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")
    DRAFT = "DRAFT", _("Draft")
    RELEASED = "RELEASED", _("Released")
    APPROVED_DRAFT = "APPROVED_DRAFT", _("Approved Draft")
    ABSENT = "ABSENT", _("Absent")
    PURCHASE_ORDER = "PURCHASE_ORDER", _("Purchase Order")
    SUSPEND = "SUSPEND", _("Suspend")
    ON_HOLD = "ON_HOLD", _("On Hold")
    HARDWIRED = "HARDWIRED", _("Hardwired")
    LOSS = "LOSS", _("Loss")
    FREEZE = "FREEZE", _("Freeze")
    FOR_ADJUSTMENT = "FOR_ADJUSTMENT", _("For Adjustment")
    DISTRIBUTOR_ORDER = "DISTRIBUTOR_ORDER", _("Distributor Order")


class UserTypeChoices(models.TextChoices):
    LEAD = "LEAD", _("Lead")
    CLIENT = "CLIENT", _("Client")
    ADVISOR = "ADVISOR", _("Advisor")
    INTRODUCER = "INTRODUCER", _("Introducer")
    SERVICE_HOLDER = "SERVICE_HOLDER", _("Service Holder")


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class RoleChoices(models.TextChoices):
    INTRODUCER = "INTRODUCER", _("Introducer")
    ADVISOR = "ADVISOR", _("Advisor")
    ADMIN = "ADMIN", _("Admin")
    LEAD = "LEAD", _("Lead")
    CLIENT = "CLIENT", _("Client")


class ProductCategoryChoices(models.TextChoices):
    MORTGAGES = "MORTGAGES", _("Mortgages")
    PROTECTION = "PROTECTION", _("Protection")
    GENERAL_INSURANCE = "GENERAL_INSURANCE", _("General Insurance")


class CaseStatusChoices(models.TextChoices):
    NEW_LEAD = "NEW_LEAD", _("New Lead")
    CALL_BACK = "CALL_BACK", _("Call Back")
    MEETING = "MEETING", _("Meeting")


class CaseStageChoices(models.TextChoices):
    INQUIRY = "INQUIRY", _("Inquiry")
    FACT_FIND = "FACT_FIND", _("Fact Find")
    RESEARCH_COMPLIANCE_CHECK = "RESEARCH_COMPLIANCE_CHECK", _(
        "Research and Compliance Check"
    )
    DECISION_IN_PRINCIPLE = "DECISION_IN_PRINCIPLE", _("Decision in Principle")
    FULL_MORTGAGE_APPLICATION = "FULL_MORTGAGE_APPLICATION", _(
        "Full Mortgage Application"
    )
    OFFER_FROM_BANK = "OFFER_FROM_BANK", _("Offer From Bank")
    LEGAL = "LEGAL", _("Legal")
    COMPLETION = "COMPLETION", _("Completion")
    FUTURE_OPPORTUNITY = "FUTURE_OPPORTUNITY", _("Future Opportunity")
    NOT_PROCEED = "NOT_PROCEED", _("Not Proceed")


class ApplicantTypeChoices(models.TextChoices):
    SINGLE = "SINGLE", _("Single")
    JOINT = "JOINT", _("Joint")
