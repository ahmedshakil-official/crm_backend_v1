from django.db import models
from django.utils.translation import gettext_lazy as _

class NameTitleChoices(models.TextChoices):
    MR = "MR", _("Mr.")
    MRS = "MRS", _("Mrs.")
    MS = "MS", _("Ms.")
    DR = "DR", _("Dr.")
    MISS = "MISS", _("Miss.")
    MADAM = "MADAM", _("Madam.")
    MAIDEN = "MAIDEN", _("Maiden.")
    PROFESSOR = "PROFESSOR", _("Professor.")
    DOCTOR = "DOCTOR", _("Doctor.")


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

    # Network-level roles
    NETWORK_CEO = "NETWORK_CEO", _("Network CEO")
    NETWORK_COO = "NETWORK_COO", _("Network COO")
    NETWORK_SYSTEM_DEVELOPER = "NETWORK_SYSTEM_DEVELOPER", _("Network System Developer")
    NETWORK_COMPLIANCE_MANAGER = "NETWORK_COMPLIANCE_MANAGER", _(
        "Network Compliance Manager"
    )
    NETWORK_COMPLIANCE_ASSISTANT = "NETWORK_COMPLIANCE_ASSISTANT", _(
        "Network Compliance Assistant"
    )
    NETWORK_PRINCIPAL_ADVISER = "NETWORK_PRINCIPAL_ADVISER", _(
        "Network Principal Adviser"
    )
    NETWORK_ADVISER = "NETWORK_ADVISER", _("Network Adviser")
    NETWORK_ADMIN = "NETWORK_ADMIN", _("Network Admin")
    NETWORK_SUPPORT = "NETWORK_SUPPORT", _("Network Support Staff")

    # Organization-level (AR Firm) roles
    ORGANIZATION_CEO = "ORGANIZATION_CEO", _("Organization CEO")
    ORGANIZATION_COO = "ORGANIZATION_COO", _("Organization COO")
    ORGANIZATION_SYSTEM_DEVELOPER = "ORGANIZATION_SYSTEM_DEVELOPER", _(
        "Organization System Developer"
    )
    ORGANIZATION_COMPLIANCE_MANAGER = "ORGANIZATION_COMPLIANCE_MANAGER", _(
        "Organization Compliance Manager"
    )
    ORGANIZATION_COMPLIANCE_ASSISTANT = "ORGANIZATION_COMPLIANCE_ASSISTANT", _(
        "Organization Compliance Assistant"
    )
    ORGANIZATION_PRINCIPAL_ADVISER = "ORGANIZATION_PRINCIPAL_ADVISER", _(
        "Organization Principal Adviser"
    )
    ORGANIZATION_ADVISER = "ORGANIZATION_ADVISER", _("Organization Adviser")
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN", _("Organization Admin")
    ORGANIZATION_SUPPORT = "ORGANIZATION_SUPPORT", _("Organization Support Staff")


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class OrganizationRoleChoices(models.TextChoices):
    INTRODUCER = "INTRODUCER", _("Introducer")
    ADVISOR = "ADVISOR", _("Advisor")
    ADMIN = "ADMIN", _("Admin")
    LEAD = "LEAD", _("Lead")
    CLIENT = "CLIENT", _("Client")
    JOINT_USER = "JOINT_USER", _("Joint User")

    # Organization-level (AR Firm) roles
    ORGANIZATION_CEO = "ORGANIZATION_CEO", _("Organization CEO")
    ORGANIZATION_COO = "ORGANIZATION_COO", _("Organization COO")
    ORGANIZATION_SYSTEM_DEVELOPER = "ORGANIZATION_SYSTEM_DEVELOPER", _(
        "Organization System Developer"
    )
    ORGANIZATION_COMPLIANCE_MANAGER = "ORGANIZATION_COMPLIANCE_MANAGER", _(
        "Organization Compliance Manager"
    )
    ORGANIZATION_COMPLIANCE_ASSISTANT = "ORGANIZATION_COMPLIANCE_ASSISTANT", _(
        "Organization Compliance Assistant"
    )
    ORGANIZATION_PRINCIPAL_ADVISER = "ORGANIZATION_PRINCIPAL_ADVISER", _(
        "Organization Principal Adviser"
    )
    ORGANIZATION_ADVISER = "ORGANIZATION_ADVISER", _("Organization Adviser")
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN", _("Organization Admin")
    ORGANIZATION_SUPPORT = "ORGANIZATION_SUPPORT", _("Organization Support Staff")


class NetworkRoleChoices(models.TextChoices):
    INTRODUCER = "INTRODUCER", _("Introducer")
    ADVISOR = "ADVISOR", _("Advisor")
    ADMIN = "ADMIN", _("Admin")
    LEAD = "LEAD", _("Lead")
    CLIENT = "CLIENT", _("Client")
    JOINT_USER = "JOINT_USER", _("Joint User")

    # Network-level roles
    NETWORK_CEO = "NETWORK_CEO", _("Network CEO")
    NETWORK_COO = "NETWORK_COO", _("Network COO")
    NETWORK_SYSTEM_DEVELOPER = "NETWORK_SYSTEM_DEVELOPER", _("Network System Developer")
    NETWORK_COMPLIANCE_MANAGER = "NETWORK_COMPLIANCE_MANAGER", _(
        "Network Compliance Manager"
    )
    NETWORK_COMPLIANCE_ASSISTANT = "NETWORK_COMPLIANCE_ASSISTANT", _(
        "Network Compliance Assistant"
    )
    NETWORK_PRINCIPAL_ADVISER = "NETWORK_PRINCIPAL_ADVISER", _(
        "Network Principal Adviser"
    )
    NETWORK_ADVISER = "NETWORK_ADVISER", _("Network Adviser")
    NETWORK_ADMIN = "NETWORK_ADMIN", _("Network Admin")
    NETWORK_SUPPORT = "NETWORK_SUPPORT", _("Network Support Staff")


class ProductCategoryChoices(models.TextChoices):
    MORTGAGE = "MORTGAGE", _("Mortgage")
    PROTECTION = "PROTECTION", _("Protection")
    GENERAL_INSURANCE = "GENERAL_INSURANCE", _("General Insurance")


class CaseStatusChoices(models.TextChoices):
    NEW_LEAD = "NEW_LEAD", _("New Lead")
    CALL_BACK = "CALL_BACK", _("Call Back")
    MEETING = "MEETING", _("Meeting")


class CaseStageChoices(models.TextChoices):
    ENQUIRY = "ENQUIRY", _("Enquiry")
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


class MeetingTypeChoices(models.TextChoices):
    UPCOMING = "UPCOMING", _("Upcoming Meeting")
    PREVIOUS = "PREVIOUS", _("Previous Meeting")


class MeetingStatusChoices(models.TextChoices):
    CONFIRMED = "CONFIRMED", _("Confirmed")
    CANCELLED = "CANCELLED", _("Canceled")
    ON_HOLD = "ON_HOLD", _("On Hold")
    SUCCESS = "SUCCESS", _("Success")


class CircumstancesObjectivesChoices(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class BudgetAffordabilityChoices(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class NewMortgageDetailsChoices(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class RecommendingRepaymentMethodChoices(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class RecommendingMortgageTypeChoices(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class RecommendingMortgageLenderChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class RecommendingMortgageAmountChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class CostsFeesChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class DisadvantageRisksChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class CostAdviceChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class ProtectionChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class BuildingsInsuranceChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class WillsChoice(models.TextChoices):
    GENERAL = "GENERAL", _("General")
    SHARIA = "SHARIA", _("Sharia")


class RemedialActionsRequiredChoices(models.TextChoices):
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class RemedialActionsCompleteChoices(models.TextChoices):
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class TermsBusinessChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class PrivacyNoticeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class FeeAgreementChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class FactfindFilledChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class NivoIDVcheckChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class FinancialSanctionsCheckedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfIDChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfAddressChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfIncomeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfDepositChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class BankStatementsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class CreditReports(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AffordabilityCalculatorChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class EvidenceOfResearchChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AgreementPrincipleChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class SignedApplicationChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class SuitabilityLetterChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class MortgageOfferChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DebtConsolidationCalculatorChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class SharedEquityDocumentationChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfLendingChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class ProofOfRepaymentChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class LoanDetailsFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasSourceOfLeadBeenRecordedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class RealisticProximityToTheAdvisorChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class PersonalDetailsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class RetirementAgeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesTheOccupationComparedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class EmploymentDetailsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasDueDiligenceBeenCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesTheStatedIncomeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesTheStatedNetIncomeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsTheClientInAnOccupationChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasPropertyPortfolioFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasPropertyDetailsFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasYourNeedsFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasRepaymentVehicleRecordedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HaveFiguresBeenInputChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsDepositComeFromSaleOfPropertyChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAdviserCompletedCalculatorChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAccountantSolicitorDetailsBeenConfirmedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasCreditCommitmentsFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsAnyCreditCommitmentsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasClientAdverseCreditChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasBudgetPlannerBeenCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAllDirectDebitsBeenRecordedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAdviserSourcedMortgageRequirementsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class FiguresStatedInMortgageRequirementsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreResultsStoredInOrderOfClientPreferenceChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsRecommendedProductShowingEvidenceResearchChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsTheAddressOnTheKFICorrectChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesFiguresFeaturesMortgageRequirementsChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesMonthlyPaymentFitWithinDisposableIncomeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreFeesDisclosedCorrectlyChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class LenderFeesAddedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasIllustrationBeenProducedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class InterestOnlyChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasProductBeenFullyCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class PersonalDetailsMatchTheFactfindChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesEmploymentIncomeDetailsMatchChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesPropertyLoanDetailsMatchChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesMortgageApplicationConfirmChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasSuitabilityLetterBeenGeneratedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class PostApplicationChangesChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsApplicantsLiveAtSeparateAddressesChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class IsReplacementSuitabilityLetterChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasReasonsForMortgageBeenPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasMeetingDiscussionBeenPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasCircumstancesObjectivesPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasBudgetAffordabilityBeenPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasNewMortgageDetailsBeenCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasMortgageSectionOnePersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasMortgageSectionTwoPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreWeRecommendingRepaymentMethodChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreWeRecommendingRepaymentTypeChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreWeRecommendingRepaymentTermChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreWeRecommendingRepaymentLenderChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreWeRecommendingRepaymentAmountChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreCostAndFeesBeenCompletedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class AreDisadvantagesRisksBeenSelectedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAdviserPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasAdviserIncludedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasProtectionSectionPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasBASectionPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class HasWillsSectionPersonalisedChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")


class DoesRecommendedProductMatchYourNeedsSectionChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")
    NA = "N/A", _("N/A")

# Client servey Choice.
class ClientServeyChoices(models.TextChoices):
    Better_Than_Expected = "BETTER_THAN_EXPECTED", _("BETTER_THAN_EXPECTED")
    AS_EXPECTED = "AS_EXPECTED", _("AS_EXPECTED")
    BELOW_EXPECTED = "BELOW_EXPECTED", _("BELOW_EXPECTED")
    NA = "N/A", _("N/A")
    NOT_MENTIONED_TO_ME = "NOT_MENTIONED_TO_ME", _("NOT_MENTIONED_TO_ME")

class DoYouLikeSomeoneToContactYouChoices(models.TextChoices):
    YES = "YES", _("YES")
    NO = "NO", _("NO")