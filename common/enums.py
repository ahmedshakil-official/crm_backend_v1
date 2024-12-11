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
    JOINT_USER = "JOINT_USER", _("Joint User")


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
    MORTGAGE = "MORTGAGE", _("Mortgage")
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



class FileTypeChoices(models.TextChoices):
    COMPLIANCE_DOCUMENTS = "COMPLIANCE_DOCUMENTS", _("Compliance Documents")
    FACT_FINDS = "FACT_FINDS", _("Fact Finds")
    IDS = "IDS", _("IDs")
    PROOF_OF_ADDRESS = "PROOF_OF_ADDRESS", _("Proof of Address")
    INCOME_DOCUMENTS = "INCOME_DOCUMENTS", _("Income Documents")
    BANK_STATEMENTS = "BANK_STATEMENTS", _("Bank Statements")
    PROOF_OF_DEPOSIT_BANK_STATEMENTS = (
        "PROOF_OF_DEPOSIT_BANK_STATEMENTS",
        _("Proof of Deposit - Bank Statements"),
    )
    DONOR_DOCUMENTS = "DONOR_DOCUMENTS", _("Donor Documents")
    CREDIT_REPORT = "CREDIT_REPORT", _("Credit Report")
    RESEARCH_DOCUMENTS = "RESEARCH_DOCUMENTS", _("Research Documents")
    LENDERS_KFI = "LENDERS_KFI", _("Lender's KFI")
    LENDERS_DIP = "LENDERS_DIP", _("Lender's DIP")
    LENDERS_FULL_MORTGAGE_APPLICATION = (
        "LENDERS_FULL_MORTGAGE_APPLICATION",
        _("Lender's Full Mortgage Application"),
    )
    LENDERS_OFFER = "LENDERS_OFFER", _("Lender's Offer")
    SUITABILITY_LETTER = "SUITABILITY_LETTER", _("Suitability Letter")
    GENERAL_INSURANCE_DOCUMENTS = (
        "GENERAL_INSURANCE_DOCUMENTS",
        _("General Insurance Documents"),
    )
    PROTECTION_DOCUMENTS = "PROTECTION_DOCUMENTS", _("Protection Documents")
    AML_AND_SANCTIONS_SEARCH = (
        "AML_AND_SANCTIONS_SEARCH",
        _("AML and Sanctions Search"),
    )
    OTHERS = "OTHERS", _("Others")