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
    JOINT_USER = "JOINT_USER", _("Joint User")


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

class  HasYourNeedsFullyCompletedChoices(models.TextChoices):
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

class ExtraAnswerChoices(models.TextChoices):
    Your_Circumstances_And_Objectives = "YOUR_CIRCUMSTANCES_AND_OBJECTIVES", _("YOUR CIRCUMSTANCES AND OBJECTIVES")
    Budget_And_Affordability = "BUDGET_AND_AFFORDABILITY", _("BUDGET AND AFFORDABILITY")
    New_Mortgage_Details = "NEW_MORTGAGE_DETAILS", _("NEW MORTGAGE DETAILS")
    Why_Are_We_Recommending_This_Repayment_Method = "WHY_ARE_WE_RECOMMENDING_THIS_REPAYMENT_METHOD", _(
        "WHY ARE WE RECOMMENDING THIS REPAYMENT METHOD?")
    Why_Are_We_Recommending_This_Mortgage_Type = "WHY_ARE_WE_RECOMMENDING_THIS_MORTGAGE_TYPE", _(
        "WHY ARE WE RECOMMENDING THIS MORTGAGE TYPE?")
    Why_Are_You_Recommending_This_Term = "WHY_ARE_YOU_RECOMMENDING_THIS_TERM", _("WHY ARE WE RECOMMENDING THIS TERM?")
    Why_Are_We_Recommending_This_Mortgage_Lender = "WHY_ARE_WE_RECOMMENDING_THIS_MORTGAGE_LENDER", _(
        "WHY ARE WE RECOMMENDING THIS MORTGAGE LENDER?")
    Why_Are_We_Recommending_This_Mortgage_Amount = "WHY_ARE_WE_RECOMMENDING_THIS_MORTGAGE_AMOUNT", _(
        "WHY ARE WE RECOMMENDING THIS MORTGAGE AMOUNT?")
    What_Are_The_Costs_And_Fees = "WHAT_ARE_THE_COSTS_AND_FEES", _("WHAT ARE THE COSTS AND FEES?")
    What_Are_The_Disadvantages_And_Risks = "WHAT_ARE_THE_DISADVANTAGES_AND_RISKS", _(
        "WHAT ARE THE DISADVANTAGES AND RISKS?")
    What_Is_The_Cost_Of_Our_Advice = "WHAT_IS_THE_COST_OF_OUR_ADVICE", _("WHAT IS THE COST OF OUR ADVICE?")
    What_Is_The_Protection = "WHAT_IS_THE_PROTECTION", _("WHAT IS THE PROTECTION?")
    What_Is_The_Buildings_Insurance = "WHAT_IS_THE_BUILDINGS_INSURANCE", _("WHAT IS THE BUILDINGS INSURANCE?")
    What_Is_The_Wills = "WHAT_IS_THE_WILLS", _("WHAT IS THE WILLS?")



