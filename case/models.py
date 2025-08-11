from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lead
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django_filters.fields import ChoiceField
from multiselectfield import MultiSelectField

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
    CircumstancesObjectivesChoices,
    BudgetAffordabilityChoices,
    NewMortgageDetailsChoices,
    RecommendingRepaymentMethodChoices,
    RecommendingMortgageTypeChoices,
    RecommendingMortgageLenderChoice,
    RecommendingMortgageAmountChoice,
    CostsFeesChoice,
    DisadvantageRisksChoice,
    CostAdviceChoice,
    ProtectionChoice,
    BuildingsInsuranceChoice,
    WillsChoice,
    RemedialActionsRequiredChoices,
    RemedialActionsCompleteChoices,
    TermsBusinessChoices,
    PrivacyNoticeChoices,
    FeeAgreementChoices,
    FactfindFilledChoices,
    NivoIDVcheckChoices,
    FinancialSanctionsCheckedChoices,
    ProofOfIDChoices,
    ProofOfAddressChoices,
    ProofOfIncomeChoices,
    ProofOfDepositChoices,
    BankStatementsChoices,
    AffordabilityCalculatorChoices,
    EvidenceOfResearchChoices,
    AgreementPrincipleChoices,
    SignedApplicationChoices,
    SuitabilityLetterChoices,
    MortgageOfferChoices,
    DebtConsolidationCalculatorChoices,
    SharedEquityDocumentationChoices,
    ProofOfLendingChoices,
    ProofOfRepaymentChoices,
    RealisticProximityToTheAdvisorChoices,
    HasSourceOfLeadBeenRecordedChoices,
    LoanDetailsFullyCompletedChoices,
    PersonalDetailsChoices,
    RetirementAgeChoices,
    DoesTheOccupationComparedChoices,
    EmploymentDetailsChoices,
    HasDueDiligenceBeenCompletedChoices,
    DoesTheStatedIncomeChoices,
    DoesTheStatedNetIncomeChoices,
    IsTheClientInAnOccupationChoices,
    HasPropertyPortfolioFullyCompletedChoices,
    HasPropertyDetailsFullyCompletedChoices,
    HasYourNeedsFullyCompletedChoices,
    HasRepaymentVehicleRecordedChoices,
    HaveFiguresBeenInputChoices,
    IsDepositComeFromSaleOfPropertyChoices,
    HasAdviserCompletedCalculatorChoices,
    HasAccountantSolicitorDetailsBeenConfirmedChoices,
    HasCreditCommitmentsFullyCompletedChoices,
    IsAnyCreditCommitmentsChoices,
    HasClientAdverseCreditChoices,
    HasBudgetPlannerBeenCompletedChoices,
    HasAllDirectDebitsBeenRecordedChoices,
    HasAdviserSourcedMortgageRequirementsChoices,
    FiguresStatedInMortgageRequirementsChoices,
    AreResultsStoredInOrderOfClientPreferenceChoices,
    IsRecommendedProductShowingEvidenceResearchChoices,
    IsTheAddressOnTheKFICorrectChoices,
    DoesFiguresFeaturesMortgageRequirementsChoices,
    DoesMonthlyPaymentFitWithinDisposableIncomeChoices,
    AreFeesDisclosedCorrectlyChoices,
    LenderFeesAddedChoices,
    HasIllustrationBeenProducedChoices,
    InterestOnlyChoices,
    HasProductBeenFullyCompletedChoices,
    PersonalDetailsMatchTheFactfindChoices,
    DoesEmploymentIncomeDetailsMatchChoices,
    DoesPropertyLoanDetailsMatchChoices,
    DoesMortgageApplicationConfirmChoices,
    HasSuitabilityLetterBeenGeneratedChoices,
    PostApplicationChangesChoices,
    IsApplicantsLiveAtSeparateAddressesChoices,
    IsReplacementSuitabilityLetterChoices,
    HasReasonsForMortgageBeenPersonalisedChoices,
    HasMeetingDiscussionBeenPersonalisedChoices,
    HasCircumstancesObjectivesPersonalisedChoices,
    HasBudgetAffordabilityBeenPersonalisedChoices,
    HasNewMortgageDetailsBeenCompletedChoices,
    HasMortgageSectionOnePersonalisedChoices,
    HasMortgageSectionTwoPersonalisedChoices,
    AreWeRecommendingRepaymentMethodChoices,
    AreWeRecommendingRepaymentTypeChoices,
    AreWeRecommendingRepaymentTermChoices,
    AreWeRecommendingRepaymentLenderChoices,
    AreWeRecommendingRepaymentAmountChoices,
    AreCostAndFeesBeenCompletedChoices,
    AreDisadvantagesRisksBeenSelectedChoices,
    HasAdviserPersonalisedChoices,
    HasAdviserIncludedChoices,
    HasProtectionSectionPersonalisedChoices,
    HasBASectionPersonalisedChoices,
    HasWillsSectionPersonalisedChoices,
    DoesRecommendedProductMatchYourNeedsSectionChoices,
    ClientServeyChoices, DoYouLikeSomeoneToContactYouChoices,
)
from organization.models import Organization, Network
from .enums import (
    ApplicationTypeChoices,
    MortgageTypeChoices,
    LoanPurposeChoices,
    LenderChoices,
    BorrowerTypeChoices,
    RepaymentMethodChoices,
    RepaymentVehicleChoices,
    InterestRateTypeChoices,
    ProductTermChoices,
    AdviceLevelChoices,
    IntroductionTypeChoices,
    IntroducerPaymentTermsChoices,
    LeadSourceChoices,
    SaleTypeChoices,
    CurrentLenderChoices,
    TitleChoices,
    GenderChoices,
    MaritalStatusChoices,
    MarketingPreferencesChoices,
    ResidentialStatus,
    MortgageType,
    RepaymentType,
    InterestType,
    ERCCompletionStatus,
    PropertyType,
    TenureType,
    RoleType,
    CompanyType,
    EmploymentStatus,
    EmploymentType,
    FrequencyChoice,
    RateTypeChoices,
    EPCRatingChoices,
    UserTypeChoices,
    PremiumPaymentChoices,
    InTrustChoices,
    GuaranteedReviewableChoices,
    PolicyCancellationChoices,
    TasksNotesChoices,
    CategoryChoices,
    TaskPriorityChoices,
    InitialRateTypeChoices,
    InitialRatePeriodTypeChoices,
    ProductClassChoices,
    ArrangementFeeAddedToLoanChoices,
    BookingFeeAddedToLoanChoices,
    DIPDecisionChoices,
    FeesChoices,
    MethodChoices,
    FeesInFeeTypeChoices,
    FeesOutFeeTypeChoices,
    SubTotalsTypeChoices,
    InsuranceTypeChoices,
    LivingCostsTypeChoices,
    UnsecuredBorrowingTypeChoices,
    PriorityDebtTypeChoices,
    DebtRepaymentTypeChoices,
    IncomeTypeChoices,
    RegionChoices,
    CountryChoices,
    PropertyTypeChoices,
    HouseTypeChoice,
    FlatTypeChoices,
    ConstructionOfWallsChoices,
    ConstructionOfRoofChoices,
    ChargeTypeChoices,
    EpcRatingChoices,
    TenureChoices,
    ListedStatusOfTheBuildingChoices,
    NewBuildWarrantyProviderChoices,
    ValuationTypeChoices,
    SelectApplicantListChoices,
    RelationshipChoices,
    PolicyTypeChoices,
    CreditCommitmentsChoices,
    TypeChoices,
    CourtOrderedChoices,
    PaidOnCompletionChoices,
    ExtraAnswerChoices,
)
from .signals import (
    create_loan_details,
    create_applicant_details,
    create_applicant_details_for_joint_user,
    create_employment_details_for_lead,
    create_employment_details_for_joint_user,
    create_adverse_for_lead,
    create_adverse_for_joint_user,
    create_property_details,
    create_budget_planner,
    create_mortgage_needs,
    create_mortgage_features,
    create_mortgage_features_for_joint_user,
    create_suitability,
    create_compliance, create_client_survey,
)
from .utils import upload_to_case_files


class Case(CreatedAtUpdatedAtBaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )
    lead = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_to_case",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, blank=True)
    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, null=True, blank=True
    )
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
        default=CaseStageChoices.ENQUIRY,
        db_index=True,
    )
    notes = models.TextField(blank=True, null=True)
    is_removed = models.BooleanField(default=False, blank=True, db_index=True)
    # Additional fields for reporting
    submitted_date = models.DateTimeField(
        null=True, blank=True, help_text="Date when case was submitted"
    )
    completed_date = models.DateTimeField(
        null=True, blank=True, help_text="Date when case was completed"
    )
    last_activity_date = models.DateTimeField(
        auto_now=True, help_text="Last activity on this case"
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.name

    def generate_case_name(self):
        # Mapping case stage choices to abbreviations
        stage_mapping = {
            "ENQUIRY": "ENQ",  # Changed from "INQUIRY" to "ENQUIRY"
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
        alias_suffix = str(self.id).zfill(8)

        return f"{stage_abbreviation}-{alias_suffix}"

    def generate_organization_report(self, request, filters):
        """Generate organization report with given filters"""
        # Implementation similar to OrganizationReportView
        cases = Case.objects.all()  # Apply appropriate filters
        return self.create_pdf_report(cases, "Organization Report", None)

    def generate_adviser_report(self, request, filters):
        """Generate adviser report with given filters"""
        # Implementation similar to AdviserReportView
        cases = Case.objects.filter(created_by=request.user)
        return self.create_pdf_report(cases, "Adviser Report", None)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        self.name = self.generate_case_name()
        super().save(update_fields=['name'])


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
    is_removed = models.BooleanField(default=False, db_index=True)

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
    is_removed = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Meeting"


class LoanDetails(CreatedAtUpdatedAtBaseModel):
    case = models.OneToOneField(
        Case,
        on_delete=models.CASCADE,
        related_name="loan_details",
        verbose_name="Related Case",
    )
    application_type = models.CharField(
        max_length=50,
        choices=ApplicationTypeChoices.choices,
        default=ApplicationTypeChoices.SELECT_APPLICATION_TYPE,
    )

    mortgage_type = models.CharField(
        max_length=50, choices=MortgageTypeChoices.choices, blank=True, null=True
    )
    loan_purpose = models.CharField(
        max_length=50, choices=LoanPurposeChoices.choices, blank=True, null=True
    )
    lender = models.CharField(
        max_length=50, choices=LenderChoices.choices, blank=True, null=True
    )
    lenders_reference = models.CharField(max_length=100, blank=True, null=True)
    borrower_type = models.CharField(
        max_length=50, choices=BorrowerTypeChoices.choices, blank=True, null=True
    )
    repayment_method = models.CharField(
        max_length=50, choices=RepaymentMethodChoices.choices, blank=True, null=True
    )
    repayment_vehicle = models.CharField(
        max_length=50, choices=RepaymentVehicleChoices.choices, blank=True, null=True
    )
    interest_rate_type = models.CharField(
        max_length=50, choices=InterestRateTypeChoices.choices, blank=True, null=True
    )
    product_term = models.CharField(
        max_length=50, choices=ProductTermChoices.choices, blank=True, null=True
    )
    property_valuation = models.PositiveIntegerField(default=0)
    purchase_price = models.PositiveIntegerField(default=0)
    loan_amount = models.PositiveIntegerField(default=0)
    estimated_value = models.PositiveIntegerField(default=0)

    ltv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    term_years = models.PositiveIntegerField(default=0)
    term_months = models.PositiveIntegerField(default=0)
    outstanding_balance = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    current_monthly_payment = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    current_lender = models.CharField(
        max_length=50, choices=CurrentLenderChoices.choices, blank=True, null=True
    )

    interest_only_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, default=0.00
    )
    original_purchase_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, default=0.00
    )
    date_of_purchase = models.DateField(null=True, blank=True)
    deposit_amount = models.PositiveIntegerField(default=0)
    deposit_source = models.CharField(max_length=255, null=True, blank=True)
    advice_level = models.CharField(
        max_length=50, choices=AdviceLevelChoices.choices, blank=True, null=True
    )

    dip_accept_date = models.DateField(blank=True, null=True)
    dip_expiry_date = models.DateField(blank=True, null=True)
    expected_completion_date = models.DateField(blank=True, null=True)
    product_expiry_date = models.DateField(blank=True, null=True)

    introduction_type = models.CharField(
        max_length=50, choices=IntroductionTypeChoices.choices, blank=True, null=True
    )
    introducer_payment_terms = models.CharField(
        max_length=50,
        choices=IntroducerPaymentTermsChoices.choices,
        blank=True,
        null=True,
    )
    introducer_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    lead_source = models.CharField(
        max_length=50, choices=LeadSourceChoices.choices, blank=True, null=True
    )
    sale_type = models.CharField(
        max_length=50, choices=SaleTypeChoices.choices, blank=True, null=True
    )
    reasons_for_capital_raising = models.TextField(blank=True, null=True)
    case_summary = models.TextField(blank=True, null=True)
    accepted_or_declined_by_lender = models.BooleanField(default=False)
    case_submitted = models.DateField(blank=True, null=True)
    valuation_instructed_date = models.DateField(blank=True, null=True)
    valuation_booked_date = models.DateField(blank=True, null=True)
    valuation_received_date = models.DateField(blank=True, null=True)
    valuation_expiry_date = models.DateField(blank=True, null=True)
    case_offered_date = models.DateField(blank=True, null=True)
    stage_expiry_date = models.DateField(blank=True, null=True)
    legals_instructed_date = models.DateField(blank=True, null=True)
    exchange_of_contracts_date = models.DateField(blank=True, null=True)
    case_completed_date = models.DateField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Loan Detail"
        verbose_name_plural = "Loan Details"

    def __str__(self):
        return f"{self.application_type} - {self.mortgage_type if self.mortgage_type else 'No Mortgage Type'}"


class ApplicantDetails(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="applicant_details",
    )
    is_company_application = models.BooleanField(default=False)

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applicant",
    )
    title = models.CharField(
        max_length=10, choices=TitleChoices.choices, default=TitleChoices.MR
    )

    maiden_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_name_change =models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    anticipated_retirement_age = models.PositiveIntegerField(default=0)
    state_retirement_age = models.PositiveIntegerField(default=0)
    is_smoker = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=6, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    nationality = CountryField(blank_label="Select Country", blank=True, null=True)
    is_dual_nationality = models.BooleanField(default=False)
    dual_nationality = CountryField(blank_label="Select Country", blank=True, null=True)
    marital_status = models.CharField(
        max_length=30,
        choices=MaritalStatusChoices.choices,
        default=MaritalStatusChoices.SINGLE,
    )
    dual_nationality_country = CountryField(
        blank_label="Select Country", blank=True, null=True
    )
    ni_number = models.CharField(max_length=20, blank=True, null=True)
    country_of_birth = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    home_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    marketing_preferences = MultiSelectField(
        choices=MarketingPreferencesChoices.choices, max_length=100, blank=True
    )
    has_dependants = models.BooleanField(default=False)
    number_of_dependants = models.PositiveIntegerField(default=0)
    date_of_arrival_uk = models.DateField(blank=True, null=True)
    indefinite_right_to_reside = models.BooleanField(default=False)
    visa_details = models.CharField(max_length=255, blank=True, null=True)
    visa_expiry_date = models.DateField(blank=True, null=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    house_number_or_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    effective_from = models.DateField(blank=True, null=True)
    time_at_address_years = models.PositiveIntegerField(default=0)
    time_at_address_months = models.PositiveIntegerField(default=0)
    residential_status = models.CharField(
        max_length=50,
        choices=ResidentialStatus.choices,
        default=ResidentialStatus.OWNER,
    )
    current_mortgage_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    property_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    owner_monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    lender = models.CharField(max_length=100, blank=True, null=True)
    mortgage_start_date = models.DateField(blank=True, null=True)
    mortgage_type = models.CharField(
        max_length=100, choices=MortgageType.choices, default=MortgageType.SECURED_LOAN
    )
    current_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    remaining_term = models.PositiveIntegerField(default=0)
    repayment_type = models.CharField(
        max_length=50,
        choices=RepaymentType.choices,
        default=RepaymentType.CAPITAL_INTEREST,
    )
    current_interest_type = models.CharField(
        max_length=50, choices=InterestType.choices, default=InterestType.FIXED
    )
    early_repayment_charge_applies = models.BooleanField(default=False)
    erc_expiry_date = models.DateField(null=True, blank=True)
    erc_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    erc_being_paid = models.BooleanField(default=False)
    mortgage_account_number = models.CharField(max_length=50, blank=True, null=True)
    being_redeemed = models.BooleanField(default=False)
    is_mortgage_portable = models.BooleanField(default=False)
    is_mortgage_being_ported = models.BooleanField(default=False)
    mortgage_not_to_complete_until_erc_ended = models.CharField(
        max_length=10, choices=ERCCompletionStatus.choices, null=True, blank=True
    )
    mortgage_charter_scheme = models.BooleanField(default=False)
    property_type = models.CharField(
        max_length=50, choices=PropertyType.choices, default=PropertyType.HOUSE
    )
    bedrooms = models.PositiveIntegerField(default=0)
    tenure = models.CharField(
        max_length=50, choices=TenureType.choices, default=TenureType.FREEHOLD
    )
    year_built = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    rental_monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    landlord_name = models.CharField(max_length=100, blank=True, null=True)
    landlord_telephone = models.CharField(max_length=20, blank=True, null=True)
    landlord_email = models.EmailField(blank=True, null=True)
    intend_to_move_into_the_new_property= models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Applicant Detail"
        verbose_name_plural = "Applicant Details"

    def __str__(self):
        return f"{self.company} ({self.applicant})"


class CompanyInfo(models.Model):
    applicant_details = models.ForeignKey(
        ApplicantDetails, on_delete=models.CASCADE, related_name="company"
    )
    company_name = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=50, unique=True)
    date_of_incorporation = models.DateField(blank=True, null=True)
    company_type = models.CharField(
        max_length=50,
        choices=CompanyType.choices,
        default=CompanyType.PRIVATE_LIMITED,
    )
    trade_business_type = models.CharField(max_length=255, blank=True, null=True)
    sic_code = models.CharField(max_length=255, blank=True, null=True)
    is_spv = models.BooleanField(default=False)

    # Address fields
    postcode = models.CharField(max_length=20, blank=True, null=True)
    house_number_or_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_registration_number})"


class Dependant(models.Model):
    applicant_details = models.ForeignKey(
        ApplicantDetails, on_delete=models.CASCADE, related_name="dependants"
    )
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.date_of_birth})"


class DirectorShareholder(models.Model):
    company = models.ForeignKey(
        CompanyInfo, on_delete=models.CASCADE, related_name="directors_shareholders"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    percentage_share = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    role = models.CharField(
        max_length=50, choices=RoleType.choices, default=RoleType.DIRECTOR
    )

    def __str__(self):
        return f"{self.full_name} - {self.role} ({self.percentage_share}%)"


class EmploymentDetails(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="employment_details",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employment_details",
    )
    employment_status = models.CharField(
        max_length=50,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED,
    )

    # For 'Employed' only:
    employment_type = models.CharField(
        max_length=50, choices=EmploymentType.choices, blank=True, null=True
    )
    occupation = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_telephone = models.CharField(max_length=255, blank=True, null=True)
    employer_email_for_reference = models.EmailField(blank=True, null=True)
    employer_postcode = models.CharField(max_length=20, blank=True, null=True)
    employer_house_name_or_number = models.CharField(
        max_length=255, blank=True, null=True
    )
    employer_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    employer_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=255, blank=True, null=True)
    employer_county = models.CharField(max_length=255, blank=True, null=True)
    employer_country = models.CharField(max_length=255, blank=True, null=True)
    employment_commenced = models.DateField(blank=True, null=True)
    employment_ended = models.DateField(blank=True, null=True)

    gross_monthly_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    net_monthly_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    is_probationary_period = models.BooleanField(default=False)
    is_income_in_foreign_currency = models.BooleanField(default=False)

    bonus = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_bonus_guaranteed = models.BooleanField(default=False)
    bonus_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    overtime = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    is_overtime_guaranteed = models.BooleanField(default=False)
    overtime_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    allowance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    is_allowance_guaranteed = models.BooleanField(default=False)
    allowance_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    # For 'Self-Employed' only:
    employment_time_year = models.PositiveIntegerField(blank=True, null=True, default=0)
    employment_time_month = models.PositiveIntegerField(
        blank=True, null=True, default=0
    )
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_telephone = models.CharField(max_length=255, blank=True, null=True)
    business_house_name_or_number = models.CharField(
        max_length=255, blank=True, null=True
    )
    business_postcode = models.CharField(max_length=20, blank=True, null=True)
    business_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    business_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    business_city = models.CharField(max_length=255, blank=True, null=True)
    business_county = models.CharField(max_length=255, blank=True, null=True)
    business_country = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(
        max_length=50, choices=CompanyType.choices, blank=True, null=True
    )
    percentage_of_business_owned = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    is_accounts_available = models.BooleanField(default=False)

    year1 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2014"
    )
    year1_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 1 (default is 0 if not provided)"
    )

    year2 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2013"
    )
    year2_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 2"
    )

    year3 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2012"
    )
    year3_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 3"
    )
    accountant_name = models.CharField(max_length=255, blank=True, null=True)
    accountant_qualifications = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dividends = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    turnover = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    # For 'Retired':
    further_details = models.TextField(blank=True, null=True)
    income_source = models.CharField(max_length=255, blank=True, null=True)

    # For 'Other':
    other_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    other_income_source = models.CharField(max_length=255, blank=True, null=True)
    other_income_start_date = models.DateField(blank=True, null=True)

    # For 'Contractor':
    contractor_industry = models.CharField(max_length=255, blank=True, null=True)
    current_contract_start = models.DateField(blank=True, null=True)
    current_contract_end = models.DateField(blank=True, null=True)
    time_contracting = models.CharField(max_length=255, blank=True, null=True)
    day_rate = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    hourly_rate = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.employment_status}"


class Adverse(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="adverse")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="adverse_user"
    )
    has_any_defaults_registered_in_the_last_six_years = models.BooleanField(
        default=False
    )

    has_any_ccj_registered_in_the_last_six_years = models.BooleanField(default=False)

    missed_any_payments_on_commitments_in_the_last_five_years = models.BooleanField(
        default=False
    )

    is_a_property_repossessed = models.BooleanField(default=False)

    has_ever_been_made_bankrupt = models.BooleanField(default=False)
    have_you_ever_entered_into_an_individual_voluntary_arrangement = (
        models.BooleanField(default=False)
    )
    is_ever_enter_into_a_debt_management_plan_or_debt_relief_order = (
        models.BooleanField(default=False)
    )

    is_ever_taken_out_a_pay_day_loan = models.BooleanField(default=False)

    is_exceeded_your_overdraft_in_the_last_three_months = models.BooleanField(
        default=False
    )
    is_direct_debit_returned_in_the_last_three_months = models.BooleanField(
        default=False
    )
    why_did_the_adverse_occur = models.CharField(max_length=500, blank=True, null=True)


class Property(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="property",
    )

    applicant = models.ManyToManyField(
        User,
        related_name="applicant_property",
    )
    is_property_owner = models.BooleanField(default=False)
    postcode = models.CharField(max_length=255)
    house_name_or_number = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)

    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    current_mortgage_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    monthly_rental_income = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_mortgage_payment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    value_at_purchase = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    date_purchased = models.DateField(null=True, blank=True)
    is_hmo = models.BooleanField(default=False)
    is_mufb = models.BooleanField(default=False)

    mortgage_lender = models.CharField(max_length=255, null=True, blank=True)
    repayment_type = models.CharField(max_length=255, null=True, blank=True)
    to_be_repaid = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    current_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rate_type = models.CharField(
        max_length=255, choices=RateTypeChoices.choices, null=True, blank=True
    )
    current_rate_end_date = models.DateField(null=True, blank=True)
    erc_end_date = models.DateField(null=True, blank=True)

    account_number = models.CharField(max_length=255, null=True, blank=True)
    property_type = models.CharField(max_length=255)
    ownership = models.CharField(max_length=255)
    leasehold = models.IntegerField(null=True, blank=True)  # Years
    year_built = models.IntegerField(null=True, blank=True)
    number_of_bedrooms = models.IntegerField()
    remaining_mortgage_term = models.IntegerField(null=True, blank=True)  # Years
    is_limited_company = models.BooleanField(default=False)
    epc_rating = models.CharField(
        max_length=255, choices=EPCRatingChoices.choices, null=True, blank=True
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Property {self.alias} - {self.property_value} ({self.city}, {self.country})"


class SolicitorAccountant(CreatedAtUpdatedAtBaseModel):

    name = models.CharField(max_length=255)
    user_type = models.CharField(
        choices=UserTypeChoices.choices,
        max_length=255,
        default=UserTypeChoices.ACCOUNTANT,
    )
    sra_number = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255)
    building_name_or_number = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    fax_number = models.CharField(max_length=255, null=True, blank=True)
    dx_number = models.CharField(max_length=255, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    number_of_partners_in_firm = models.IntegerField(null=True, blank=True)
    qualifications = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"SolicitorAccountant {self.alias} - {self.user_type} - {self.sra_number} ({self.city}, {self.country})"


class CaseSolicitor(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="solicitor_case"
    )
    solicitor = models.ForeignKey(
        SolicitorAccountant,
        on_delete=models.CASCADE,
        related_name="solicitor_case_user",
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.solicitor} - {self.case}"


class CaseAccountant(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="accountant_case"
    )
    accountant = models.ForeignKey(
        SolicitorAccountant,
        on_delete=models.CASCADE,
        related_name="accountant_case_user",
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.accountant} - {self.case}"


# existing-protection
class ExistingProtection(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="existing_protection",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="protection_user"
    )
    have_any_existing_Protection_policies_in_place = models.BooleanField(default=False)
    policy_type = models.CharField(
        max_length=255, choices=PolicyTypeChoices.choices, null=True, blank=True
    )
    policy_provider = models.CharField(max_length=255, null=True, blank=True)
    insurers_reference = models.CharField(max_length=255, null=True, blank=True)
    sum_assured = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    premium = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    premium_payment_type = models.CharField(
        max_length=255, choices=PremiumPaymentChoices.choices, null=True, blank=True
    )
    person_assured = models.CharField(max_length=255, null=True, blank=True)
    in_trust = models.CharField(
        max_length=255, choices=InTrustChoices.choices, null=True, blank=True
    )
    guaranteed_reviewable = models.CharField(
        max_length=255,
        choices=GuaranteedReviewableChoices.choices,
        null=True,
        blank=True,
    )
    remaining_policy_term = models.CharField(max_length=255, null=True, blank=True)
    cancelled_lapsed_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    date_policy_started = models.DateField(null=True, blank=True)
    waiver_of_premium = models.BooleanField(default=False)
    indexation = models.BooleanField(default=False)
    death_in_service_provision = models.BooleanField(default=False)
    have_non_standard_terms_been_issued = models.BooleanField(default=False)
    copy_and_paste_non_standard_terms_from_lender = models.TextField(
        null=True, blank=True
    )
    will_this_policy_be_cancelled = models.BooleanField(default=False)
    reason_for_policy_cancellation = models.CharField(
        max_length=255, choices=PolicyCancellationChoices.choices, null=True, blank=True
    )
    policy_cancellation_notes = models.TextField(null=True, blank=True)
    why_did_you_take_out_this_policy = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"ExistingProtection {self.alias} - {self.policy_type} - {self.policy_provider}"


class Notes(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="notes_related",
    )
    note_task = models.CharField(
        max_length=255,
        choices=TasksNotesChoices.choices,
        default=TasksNotesChoices.NOTE,
    )
    note_visible_to_introducer = models.BooleanField(default=False)
    note_visible_to_client = models.BooleanField(default=False)
    category = models.CharField(
        max_length=255, choices=CategoryChoices.choices, null=True, blank=True
    )
    task_priority = models.CharField(
        max_length=255, choices=TaskPriorityChoices.choices, null=True, blank=True
    )
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=1500, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return (
            f"Notes {self.alias} - {self.note_task} - {self.note_visible_to_introducer}"
        )


class Product(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="products",
    )
    product_description = models.CharField(max_length=255, null=True, blank=True)
    initial_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    initial_rate_type = models.CharField(
        max_length=255,
        choices=InitialRateTypeChoices.choices,
        default=InitialRateTypeChoices.PLEASE_SELECT_A_INITIAL_RATE_TYPE,
    )
    initial_rate_period_type = models.CharField(
        max_length=255,
        choices=InitialRatePeriodTypeChoices.choices,
        default=InitialRatePeriodTypeChoices.PLEASE_SELECT_A_INITIAL_RATE_PERIOD_TYPE,
    )
    reversion_rate = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    initial_rate_period = models.PositiveIntegerField(null=True, blank=True)
    initial_rate_date_period = models.DateField(null=True, blank=True)
    max_ltv = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    annual_percentage_rate = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    product_class = models.CharField(
        max_length=255,
        choices=ProductClassChoices.choices,
        null=True,
        blank=True,
        default=ProductClassChoices.PLEASE_SELECT_A_PRODUCT_CLASS,
    )
    early_repayment_charge = models.PositiveIntegerField(null=True, blank=True)
    early_repayment_charge_end_date = models.DateField(null=True, blank=True)
    initial_monthly_payment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    initial_monthly_payment_including_fees = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    monthly_payment_after_initial_Period = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    true_cost_over_initial_period = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    true_cost_over_term = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    true_cost_without_fees = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    loan_required_including_fees = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    arrangement_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    arrangement_fee_added_to_loan = models.CharField(
        max_length=255,
        choices=ArrangementFeeAddedToLoanChoices.choices,
        default=ArrangementFeeAddedToLoanChoices.SELECT,
    )
    valuation_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    booking_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    booking_fee_added_to_loan = models.CharField(
        max_length=255,
        choices=BookingFeeAddedToLoanChoices.choices,
        default=BookingFeeAddedToLoanChoices.SELECT,
    )
    procuration_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    processing_consent = models.BooleanField(default=False)
    processing_consent_description = models.TextField(null=True, blank=True)
    application_review = models.BooleanField(default=False)
    application_review_description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Product {self.product_class} - {self.product_description}"


class DipHistory(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="dip_history",
    )
    is_this_application_had_a_decision_in_principle = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    lender = models.CharField(
        max_length=255,
        choices=LenderChoices.choices,
        default=LenderChoices.ACCORD_MORTGAGES,
    )
    dip_date = models.DateField(null=True, blank=True)
    dip_decision = models.CharField(
        max_length=255,
        choices=DIPDecisionChoices.choices,
        default=DIPDecisionChoices.ACCEPTED,
    )
    dip_reference_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"DipHistory {self.dip_decision} - {self.dip_date}"


class Fees(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="fees",
    )
    fees_type = models.CharField(
        max_length=255, choices=FeesChoices.choices, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fee_in_type = models.CharField(
        max_length=255, choices=FeesInFeeTypeChoices.choices, null=True, blank=True
    )
    fee_out_type = models.CharField(
        max_length=255, choices=FeesOutFeeTypeChoices.choices, null=True, blank=True
    )
    method = models.CharField(
        max_length=255,
        choices=MethodChoices.choices,
        default=MethodChoices.CREDIT_DEBIT_CARD,
    )
    notes = models.CharField(max_length=500, null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)
    date_paid_out = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Fees {self.fees} - {self.amount}"


class Income(CreatedAtUpdatedAtBaseModel):
    income_type = models.CharField(
        max_length=255,
        choices=IncomeTypeChoices.choices,
        default=IncomeTypeChoices.CURRENT_INCOME,
    )
    applicant_one_net_monthly_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    applicant_two_net_monthly_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    rental_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    part_time_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    jobseekers_allowance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    child_benefit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tax_credits = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    working_tax_credits = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    maintenance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    pension = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_benefits = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Income ({self.income_type}) - Total: £{self.total_income}"


# Model for Debt Repayments
class DebtRepayments(CreatedAtUpdatedAtBaseModel):
    repayment_type = models.CharField(
        max_length=50,
        choices=DebtRepaymentTypeChoices.choices,
        default=DebtRepaymentTypeChoices.CURRENT_DEBT_REPAYMENTS,
    )

    mortgage_rent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    second_mortgage = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    shared_ownership_rental = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_debt_repayment = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Debt Repayments ({self.repayment_type}) - Total: £{self.total_debt_repayment}"


class PriorityDebt(CreatedAtUpdatedAtBaseModel):
    debt_type = models.CharField(
        max_length=50,
        choices=PriorityDebtTypeChoices.choices,
        default=PriorityDebtTypeChoices.CURRENT_PRIORITY_DEBT,
    )

    mortgage_arrears = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    gas_arrears = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    maintenance_arrears = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    defaults = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    ccjs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    debt_management_plans = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    magistrate_court_fines = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    council_tax_arrears = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_priority_debt = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Priority Debt ({self.debt_type}) - Total: £{self.total_priority_debt}"


# Model for Unsecured Borrowing
class UnsecuredBorrowing(CreatedAtUpdatedAtBaseModel):
    borrowing_type = models.CharField(
        max_length=50,
        choices=UnsecuredBorrowingTypeChoices.choices,
        default=UnsecuredBorrowingTypeChoices.CURRENT_UNSECURED_BORROWING,
    )

    credit_cards = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    loans = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    car_finance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    overdraft = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    store_cards = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    student_loans = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_borrowing = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_unsecured_borrowing = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Unsecured Borrowing ({self.borrowing_type}) - Total: £{self.total_unsecured_borrowing}"


class LivingCosts(CreatedAtUpdatedAtBaseModel):
    cost_type = models.CharField(
        max_length=50,
        choices=LivingCostsTypeChoices.choices,
        default=LivingCostsTypeChoices.CURRENT_LIVING_COSTS,
    )

    electricity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    gas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    water = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    landline_mobile_phone = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tv_license = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    council_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    ground_rent_service_charges = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    buildings_contents = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    mortgage_payment_protection = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    endowment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    pension_contribution = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    childcare = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    maintenance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    food = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    car_maintenance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    fuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    public_transport = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tv_broadband = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    recreation_holidays = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    clothing = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    medical_expenses = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    education = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_living_costs = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_living_expenses = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Living Costs ({self.cost_type}) - Total: £{self.total_living_expenses}"


# Model for Insurances
class Insurances(CreatedAtUpdatedAtBaseModel):
    insurance_type = models.CharField(
        max_length=50,
        choices=InsuranceTypeChoices.choices,
        default=InsuranceTypeChoices.CURRENT_INSURANCES,
    )

    motor_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    health_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    payment_protection = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    life_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    dental_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_insurance_expenses = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Insurances ({self.insurance_type}) - Total: £{self.total_insurance_expenses}"


class SubTotals(CreatedAtUpdatedAtBaseModel):
    subtotal_type = models.CharField(
        max_length=50,
        choices=SubTotalsTypeChoices.choices,
        default=SubTotalsTypeChoices.CURRENT_SUB_TOTALS,
    )

    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_debt_repayment = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )
    total_living_expenses = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )
    available_income = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"SubTotals ({self.subtotal_type}) - Available Income: £{self.available_income}"


# create PropertyDetails model.
class PropertyDetails(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="property_details",
    )
    property_purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    property_estimated_valuation = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    have_you_found_a_property_yet = models.BooleanField(default=False)
    notes = models.CharField(max_length=500, null=True, blank=True)
    postcode = models.CharField(max_length=50, null=True, blank=True)
    house_name_or_number = models.CharField(max_length=100, null=True, blank=True)
    address_one = models.CharField(max_length=100, null=True, blank=True)
    address_two = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(
        max_length=50,
        choices=RegionChoices.choices,
        default=RegionChoices.PLEASE_SELECT_A_REGION,
    )
    country = models.CharField(
        max_length=50,
        choices=CountryChoices.choices,
        default=CountryChoices.UNITED_KINGDOM,
    )
    property_type = models.CharField(
        max_length=50,
        choices=PropertyTypeChoices.choices,
        default=PropertyTypeChoices.SELECT,
        blank=False,
    )
    house_type = models.CharField(
        max_length=50,
        choices=HouseTypeChoice.choices,
        default=HouseTypeChoice.SELECT,
        blank=False,
    )
    flat_type = models.CharField(
        max_length=50, choices=FlatTypeChoices.choices, default=FlatTypeChoices.SELECT
    )
    construction_of_walls = models.CharField(
        max_length=50,
        choices=ConstructionOfWallsChoices.choices,
        default=ConstructionOfWallsChoices.PLEASE_SELECT_A_CONSTRUCTION_TYPE,
    )
    construction_of_roof = models.CharField(
        max_length=50, choices=ConstructionOfRoofChoices.choices, null=True, blank=True
    )
    bedrooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    bathrooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    reception_rooms = models.PositiveIntegerField(default=0, null=True, blank=True)
    kitchens = models.PositiveIntegerField(default=0, null=True, blank=True)
    garages = models.PositiveIntegerField(default=0, null=True, blank=True)
    parking_spaces = models.PositiveIntegerField(default=0, null=True, blank=True)
    charge_type = models.CharField(
        max_length=50, choices=ChargeTypeChoices.choices, default=ChargeTypeChoices.ONE
    )
    epc_rating = models.CharField(
        max_length=50, choices=EpcRatingChoices.choices, default=EpcRatingChoices.SELECT
    )
    floor = models.PositiveIntegerField(default=0)
    flats = models.PositiveIntegerField(default=0)
    number_of_storeys_in_the_building = models.PositiveIntegerField(default=0)
    year_built = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)], default=1
    )
    lift_access = models.BooleanField(default=False)
    tenure = models.CharField(
        max_length=50, choices=TenureChoices.choices, default=TenureChoices.SELECT
    )
    property_lease_term = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    service_charge_per_month = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    ground_rent_per_annum = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    residential = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    commercial = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    is_the_property_a_listed_building = models.BooleanField(default=False)
    number_of_units = models.PositiveIntegerField(null=True, blank=True)
    listed_status_of_the_building = models.CharField(
        max_length=50,
        choices=ListedStatusOfTheBuildingChoices.choices,
        default=ListedStatusOfTheBuildingChoices.SELECT,
    )
    listed_building_notes = models.CharField(max_length=500, null=True, blank=True)
    do_you_or_will_you_own_part_or_all_of_the_freehold = models.BooleanField(
        default=False
    )
    is_the_property_part_of_a_help_to_buy_shared_ownership_scheme = models.BooleanField(
        default=False
    )
    is_the_property_above_or_near_commercial_premises = models.BooleanField(
        default=False
    )
    is_the_property_a_new_build = models.BooleanField(default=False)
    new_build_warranty_provider = models.CharField(
        max_length=50,
        choices=NewBuildWarrantyProviderChoices.choices,
        default=NewBuildWarrantyProviderChoices.SELECT_WARRANTY_PROVIDER,
    )
    other_new_build_warranty_rovider = models.CharField(
        max_length=50, null=True, blank=True
    )
    is_the_property_a_right_to_buy = models.BooleanField(default=False)
    date_of_purchase = models.DateField(null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    is_the_property_ex_local_authority = models.BooleanField(default=False)
    is_this_property_being_purchased_from_the_council_with_this_application = (
        models.BooleanField(default=False, db_column="purchased_from_council_with_app")
    )
    is_there_an_annexe_within_the_property = models.BooleanField(default=False)
    will_the_property_be_owner_occupied = models.BooleanField(default=False)
    please_provide_further_details = models.CharField(
        max_length=255, null=True, blank=True
    )
    is_the_property_on_the_market = models.BooleanField(default=False)
    is_the_property_rented_out_to_be_rented_out = models.BooleanField(default=False)
    is_the_property_standard_construction = models.BooleanField(default=False)
    comments_details = models.CharField(max_length=255, null=True, blank=True)
    does_the_property_have_solar_panels = models.BooleanField(default=False)
    do_you_own_the_solar_panels = models.BooleanField(default=False)
    is_the_property_used_purely_for_residential_purposes = models.BooleanField(
        default=False
    )
    valuation_type = models.CharField(
        max_length=50, choices=ValuationTypeChoices.choices, null=True, blank=True
    )
    select_applicant_list = models.CharField(
        max_length=50,
        choices=SelectApplicantListChoices.choices,
        default=SelectApplicantListChoices.SELECT,
    )
    contact_for_access = models.CharField(max_length=50, null=True, blank=True)
    contacts_name = models.CharField(max_length=50, null=True, blank=True)
    contacts_daytime_telephone = models.CharField(max_length=20, null=True, blank=True)
    contacts_mobile_telephone = models.CharField(max_length=20, null=True, blank=True)
    contacts_email_address = models.CharField(max_length=50, null=True, blank=True)

    estimated_value = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.house_name_or_number}"


class OtherOccupants(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="other_occupants",
    )
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    relationship = models.CharField(
        max_length=50,
        choices=RelationshipChoices.choices,
        default=RelationshipChoices.PARTNER,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.full_name} - {self.date_of_birth}"


class BudgetPlanner(CreatedAtUpdatedAtBaseModel):
    case = models.OneToOneField(
        Case, on_delete=models.CASCADE, related_name="budget_planner"
    )
    current_income = models.OneToOneField(
        Income,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_income",
    )
    post_income = models.OneToOneField(
        Income,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_income",
    )
    current_debt_repayments = models.OneToOneField(
        DebtRepayments,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_debt_repayments",
    )
    post_debt_repayments = models.OneToOneField(
        DebtRepayments,
        on_delete=models.CASCADE,
        related_name="post_debt_repayments",
        null=True,
        blank=True,
    )
    current_priority_debt = models.OneToOneField(
        PriorityDebt,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_priority_debt",
    )
    post_priority_debt = models.OneToOneField(
        PriorityDebt,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_priority_debt",
    )
    current_unsecured_borrowing = models.OneToOneField(
        UnsecuredBorrowing,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_unsecured_borrowing",
    )
    post_unsecured_borrowing = models.OneToOneField(
        UnsecuredBorrowing,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_unsecured_borrowing",
    )
    current_living_cost = models.OneToOneField(
        LivingCosts,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_living_cost",
    )
    post_living_cost = models.OneToOneField(
        LivingCosts,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_living_cost",
    )
    current_insurance = models.OneToOneField(
        Insurances,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_insurance",
    )
    post_insurance = models.OneToOneField(
        Insurances,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_insurance",
    )
    current_sub_total = models.OneToOneField(
        SubTotals,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_sub_total",
    )
    post_sub_total = models.OneToOneField(
        SubTotals,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_sub_total",
    )
    disclaimer = models.BooleanField(default=False)
    disclaimer_details = models.CharField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")


class CreditCommitments(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="credit_commitments"
    )
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applicant_credit_commitments"
    )
    joint = models.CharField(
        max_length=20, choices=CreditCommitmentsChoices.choices, null=True, blank=True
    )
    type = models.CharField(
        max_length=20, choices=TypeChoices.choices, null=True, blank=True
    )
    company = models.CharField(max_length=50, null=True, blank=True)
    account_no = models.CharField(null=True, blank=True)
    os_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    settlement_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    monthly_repayment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    card_limit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    term_remaining = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    balloon_payment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    court_ordered = models.CharField(
        max_length=50, choices=CourtOrderedChoices.choices, null=True, blank=True
    )
    cost_of_credit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    paid_on_completion = models.CharField(
        max_length=50, choices=PaidOnCompletionChoices.choices, null=True, blank=True
    )
    source = models.CharField(max_length=100, null=True, blank=True)
    has_the_unsecured_credit_mounted_up = models.CharField(
        max_length=255, null=True, blank=True
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.company} {self.source} - {self.account_no}"


class MortgageNeeds(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="mortgage_needs"
    )
    repayment_method = models.CharField(max_length=10000, null=True, blank=True)
    monthly_mortgage_payments = models.CharField(
        max_length=10000, null=True, blank=True
    )
    specific_mortgage_deal = models.CharField(max_length=10000, null=True, blank=True)
    referred_monthly_budget = models.CharField(max_length=10000, null=True, blank=True)
    retirement_age = models.CharField(max_length=10000, null=True, blank=True)
    what_suitable_mortgage_features_are_important = models.CharField(
        max_length=10000, null=True, blank=True
    )
    front_costs = models.BooleanField(default=False)
    is_ability_to_make_overpayments = models.BooleanField(default=False)
    is_early_repayment_charges = models.BooleanField(default=False)
    is_minimise_any_lender_arrangement_costs = models.BooleanField(default=False)
    is_ability_to_add_fees_to_the_mortgage = models.BooleanField(default=False)
    is_ability_to_add_fees_mortgage_extra_interest_will_be_payable = (
        models.BooleanField(default=False)
    )
    note_one = models.CharField(max_length=10000, null=True, blank=True)
    cashback = models.BooleanField(default=False)
    portability = models.BooleanField(default=False)
    guarantor_jbsp = models.BooleanField(default=False)
    offset_mortgage = models.BooleanField(default=False)
    scheme_specific = models.BooleanField(default=False)
    speed_of_completion = models.BooleanField(default=False)
    sharia_compliant_mortgages = models.BooleanField(default=False)
    ltd_company_btl = models.BooleanField(default=False)
    any_incentives = models.BooleanField(default=False)
    note_two = models.CharField(max_length=10000, null=True, blank=True)
    considering_debt_consolidation = models.CharField(
        max_length=10000, null=True, blank=True
    )
    anticipate_any_changes = models.BooleanField(default=False)
    anticipate_any_changes_notes = models.CharField(
        max_length=10000, null=True, blank=True
    )
    app_one_life_cover = models.BooleanField(default=False)
    app_one_critical_illness = models.BooleanField(default=False)
    app_one_income_protection = models.BooleanField(default=False)
    app_one_asu = models.BooleanField(default=False)
    app_one_pmi = models.BooleanField(default=False)
    app_one_family_income_benefit = models.BooleanField(default=False)
    app_one_buildings_and_contents = models.BooleanField(default=False)

    app_two_life_cover = models.BooleanField(default=False)
    app_two_critical_illness = models.BooleanField(default=False)
    app_two_income_protection = models.BooleanField(default=False)
    app_two_asu = models.BooleanField(default=False)
    app_two_pmi = models.BooleanField(default=False)
    app_two_family_income_benefit = models.BooleanField(default=False)
    app_two_buildings_and_contents = models.BooleanField(default=False)

    buildings = models.BooleanField(default=False)
    contents = models.BooleanField(default=False)
    accidental_damage = models.BooleanField(default=False)
    landlords_cover = models.BooleanField(default=False)
    home_emergency_cover = models.BooleanField(default=False)
    personal_possessions_cover = models.BooleanField(default=False)
    personal_possessions_confirm = models.BooleanField(default=False)
    have_you_a_will_in_place = models.BooleanField(default=False)
    have_you_a_will_in_place_note = models.CharField(
        max_length=10000, null=True, blank=True
    )
    mortgage_requirements_note = models.CharField(
        max_length=10000, null=True, blank=True
    )
    mortgage_requirements = models.BooleanField(default=False)
    note_three = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.repayment_method}"


class MortgageFeatures(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="mortgage_features"
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mortgage_features_applicant",
        null=True,
        blank=True,
    )
    life_cover = models.BooleanField(default=False)
    critical_illness = models.BooleanField(default=False)
    income_protection = models.BooleanField(default=False)
    asu = models.BooleanField(default=False)
    pmi = models.BooleanField(default=False)
    family_income_benefit = models.BooleanField(default=False)
    buildings_and_contents = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.life_cover} {self.critical_illness} {self.income_protection}"


class ExtraQuestion(CreatedAtUpdatedAtBaseModel):
    answer = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return (
            f"Extra Question: {self.answer[:50]}"
            if self.answer
            else "No answer provided"
        )

    class Meta:
        ordering = ("-created_at", "-updated_at")


class CircumstancesObjectives(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=710000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=710000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=710000, null=True, blank=True)
    question_two = models.CharField(max_length=710000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=710000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=710000, null=True, blank=True)
    question_three = models.CharField(max_length=710000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=710000, null=True, blank=True)

    circumstances_type = models.CharField(
        max_length=20,
        choices=CircumstancesObjectivesChoices.choices,
        default=CircumstancesObjectivesChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class BudgetAffordability(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=710000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)

    budget_affordability_type = models.CharField(
        max_length=20,
        choices=BudgetAffordabilityChoices.choices,
        default=BudgetAffordabilityChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class NewMortgageDetails(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)

    new_mortgage_details_type = models.CharField(
        max_length=20,
        choices=NewMortgageDetailsChoices.choices,
        default=NewMortgageDetailsChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class RecommendingRepaymentMethod(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_four = models.CharField(max_length=10000, null=True, blank=True)
    question_four_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_five = models.CharField(max_length=10000, null=True, blank=True)
    question_five_answer = models.CharField(max_length=10000, null=True, blank=True)

    recommending_repayment_method_type = models.CharField(
        max_length=20,
        choices=RecommendingRepaymentMethodChoices.choices,
        default=RecommendingRepaymentMethodChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class RecommendingMortgageType(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_four = models.CharField(max_length=10000, null=True, blank=True)
    question_four_answer = models.CharField(max_length=10000, null=True, blank=True)

    recommending_mortgage_type = models.CharField(
        max_length=20,
        choices=RecommendingMortgageTypeChoices.choices,
        default=RecommendingMortgageTypeChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class RecommendingTerm(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)

    recommending_term = models.CharField(
        max_length=20,
        choices=RecommendingMortgageTypeChoices.choices,
        default=RecommendingMortgageTypeChoices.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one}"


class RecommendingMortgageLender(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)

    recommending_mortgage_lender_type = models.CharField(
        max_length=20,
        choices=RecommendingMortgageLenderChoice.choices,
        default=RecommendingMortgageLenderChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class RecommendingMortgageAmount(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)

    recommending_mortgage_amount = models.CharField(
        max_length=20,
        choices=RecommendingMortgageAmountChoice.choices,
        default=RecommendingMortgageAmountChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class CostsFees(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)

    costs_fees = models.CharField(
        max_length=20, choices=CostsFeesChoice.choices, default=CostsFeesChoice.GENERAL
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class DisadvantageRisks(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_four = models.CharField(max_length=10000, null=True, blank=True)
    question_four_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_five = models.CharField(max_length=10000, null=True, blank=True)
    question_five_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_six = models.CharField(max_length=10000, null=True, blank=True)
    question_six_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_seven = models.CharField(max_length=10000, null=True, blank=True)
    question_seven_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_eight = models.CharField(max_length=10000, null=True, blank=True)
    question_eight_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_nine = models.CharField(max_length=10000, null=True, blank=True)
    question_nine_answer = models.CharField(max_length=10000, null=True, blank=True)

    disadvantage_risks = models.CharField(
        max_length=20,
        choices=DisadvantageRisksChoice.choices,
        default=DisadvantageRisksChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two} {self.question_three}"


class CostAdvice(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)

    cost_advice = models.CharField(
        max_length=20,
        choices=CostAdviceChoice.choices,
        default=CostAdviceChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class Protection(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_four = models.CharField(max_length=10000, null=True, blank=True)
    question_four_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_four_sharia = models.CharField(max_length=10000, null=True, blank=True)

    protection = models.CharField(
        max_length=20,
        choices=ProtectionChoice.choices,
        default=ProtectionChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class BuildingsInsurance(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_two_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_four = models.CharField(max_length=10000, null=True, blank=True)
    question_four_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_five_sharia = models.CharField(max_length=10000, null=True, blank=True)

    buildings_insurance = models.CharField(
        max_length=20,
        choices=BuildingsInsuranceChoice.choices,
        default=BuildingsInsuranceChoice.GENERAL,
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class Wills(CreatedAtUpdatedAtBaseModel):
    question_one = models.CharField(max_length=10000, null=True, blank=True)
    question_one_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_one_sharia = models.CharField(max_length=10000, null=True, blank=True)
    question_two = models.CharField(max_length=10000, null=True, blank=True)
    question_two_answer = models.CharField(max_length=10000, null=True, blank=True)
    question_three = models.CharField(max_length=10000, null=True, blank=True)
    question_three_answer = models.CharField(max_length=10000, null=True, blank=True)

    wills = models.CharField(
        max_length=20, choices=WillsChoice.choices, default=WillsChoice.GENERAL
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.question_one} {self.question_two}"


class Suitability(CreatedAtUpdatedAtBaseModel):
    case = models.OneToOneField(
        Case, on_delete=models.CASCADE, related_name="suitability"
    )
    circumstances_objectives = models.OneToOneField(
        CircumstancesObjectives,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_circumstances",
    )
    budget_affordability = models.OneToOneField(
        BudgetAffordability,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_budget_affordability",
    )
    new_mortgage_details = models.OneToOneField(
        NewMortgageDetails,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_new_mortgage_details",
    )
    recommending_repayment_method = models.OneToOneField(
        RecommendingRepaymentMethod,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_recommending_repayment_method",
    )
    recommending_mortgage_type = models.OneToOneField(
        RecommendingMortgageType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_recommending_mortgage_type",
    )
    recommending_term = models.OneToOneField(
        RecommendingTerm,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_recommending_term",
    )
    recommending_mortgage_lender = models.OneToOneField(
        RecommendingMortgageLender,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_recommending_mortgage_lender",
    )
    recommending_mortgage_amount = models.OneToOneField(
        RecommendingMortgageAmount,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_recommending_mortgage_amount",
    )
    costs_fees = models.OneToOneField(
        CostsFees,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_costs_fees",
    )
    disadvantage_risks = models.OneToOneField(
        DisadvantageRisks,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_disadvantage_risks",
    )
    cost_advice = models.OneToOneField(
        CostAdvice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_cost_advice",
    )
    protection = models.OneToOneField(
        Protection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_protection",
    )
    buildings_insurance = models.OneToOneField(
        BuildingsInsurance,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_buildingsInsurance",
    )
    wills = models.OneToOneField(
        Wills,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="suitability_wills",
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")


class ExtraAnswer(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="other_questions"
    )
    section_choices = models.CharField(
        max_length=250, choices=ExtraAnswerChoices.choices, null=True, blank=True
    )
    answer = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.answer}"


class Compliance(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="compliance")
    date_file_checked = models.DateField(null=True, blank=True)
    date_file_rechecked = models.DateField(null=True, blank=True)
    file_checked = models.PositiveIntegerField(null=True, blank=True)
    remedial_actions_required = models.CharField(
        max_length=20,
        choices=RemedialActionsRequiredChoices.choices,
        null=True,
        blank=True,
    )
    remedial_actions_complete = models.CharField(
        max_length=20,
        choices=RemedialActionsCompleteChoices.choices,
        null=True,
        blank=True,
    )
    comments = models.TextField(max_length=1000, null=True, blank=True)
    rating_a = models.BooleanField(default=False)
    rating_b = models.BooleanField(default=False)
    rating_c = models.BooleanField(default=False)
    terms_of_business = models.CharField(
        max_length=20, choices=TermsBusinessChoices.choices, null=True, blank=True
    )
    terms_of_business_text = models.TextField(max_length=255, null=True, blank=True)
    privacy_notice = models.CharField(
        max_length=20, choices=PrivacyNoticeChoices.choices, null=True, blank=True
    )
    privacy_notice_text = models.TextField(max_length=255, null=True, blank=True)
    fee_agreement = models.CharField(
        max_length=20, choices=FeeAgreementChoices.choices, null=True, blank=True
    )
    fee_agreement_text = models.TextField(max_length=255, null=True, blank=True)
    factfind_filled = models.CharField(
        max_length=20, choices=FactfindFilledChoices.choices, null=True, blank=True
    )
    factfind_filled_text = models.TextField(max_length=255, null=True, blank=True)
    nivo_idv_check = models.CharField(
        max_length=20, choices=NivoIDVcheckChoices.choices, null=True, blank=True
    )
    nivo_idv_check_text = models.TextField(max_length=255, null=True, blank=True)
    financial_sanctions_checked = models.CharField(
        max_length=20,
        choices=FinancialSanctionsCheckedChoices.choices,
        null=True,
        blank=True,
    )
    financial_sanctions_checked_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    proof_of_id = models.CharField(
        max_length=20, choices=ProofOfIDChoices.choices, null=True, blank=True
    )
    proof_of_id_text = models.TextField(max_length=255, null=True, blank=True)
    proof_of_address = models.CharField(
        max_length=20, choices=ProofOfAddressChoices.choices, null=True, blank=True
    )
    proof_of_address_text = models.TextField(max_length=255, null=True, blank=True)
    proof_of_income = models.CharField(
        max_length=20, choices=ProofOfIncomeChoices.choices, null=True, blank=True
    )
    proof_of_income_text = models.TextField(max_length=255, null=True, blank=True)
    proof_of_deposit = models.CharField(
        max_length=20, choices=ProofOfDepositChoices.choices, null=True, blank=True
    )
    proof_of_deposit_text = models.TextField(max_length=255, null=True, blank=True)
    bank_statements = models.CharField(
        max_length=20, choices=BankStatementsChoices.choices, null=True, blank=True
    )
    bank_statements_text = models.TextField(max_length=255, null=True, blank=True)
    credit_reports = models.CharField(
        max_length=20, choices=BankStatementsChoices.choices, null=True, blank=True
    )
    credit_reports_text = models.TextField(max_length=255, null=True, blank=True)
    affordability_calculator = models.CharField(
        max_length=20,
        choices=AffordabilityCalculatorChoices.choices,
        null=True,
        blank=True,
    )
    affordability_calculator_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    evidence_of_research = models.CharField(
        max_length=20, choices=EvidenceOfResearchChoices.choices, null=True, blank=True
    )
    evidence_of_research_text = models.TextField(max_length=255, null=True, blank=True)
    agreement_in_principle = models.CharField(
        max_length=20, choices=AgreementPrincipleChoices.choices, null=True, blank=True
    )
    agreement_in_principle_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    signed_application = models.CharField(
        max_length=20, choices=SignedApplicationChoices.choices, null=True, blank=True
    )
    signed_application_text = models.TextField(max_length=255, null=True, blank=True)
    suitability_letter = models.CharField(
        max_length=20, choices=SuitabilityLetterChoices.choices, null=True, blank=True
    )
    suitability_letter_text = models.TextField(max_length=255, null=True, blank=True)
    mortgage_offer = models.CharField(
        max_length=20, choices=MortgageOfferChoices.choices, null=True, blank=True
    )
    mortgage_offer_text = models.TextField(max_length=255, null=True, blank=True)
    debt_consolidation_calculator = models.CharField(
        max_length=20,
        choices=DebtConsolidationCalculatorChoices.choices,
        null=True,
        blank=True,
    )
    debt_consolidation_calculator_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    shared_equity_documentation = models.CharField(
        max_length=20,
        choices=SharedEquityDocumentationChoices.choices,
        null=True,
        blank=True,
    )
    shared_equity_documentation_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    proof_of_lending = models.CharField(
        max_length=20, choices=ProofOfLendingChoices.choices, null=True, blank=True
    )
    proof_of_lending_text = models.TextField(max_length=255, null=True, blank=True)
    proof_of_repayment = models.CharField(
        max_length=20, choices=ProofOfRepaymentChoices.choices, null=True, blank=True
    )
    proof_of_repayment_text = models.TextField(max_length=255, null=True, blank=True)
    loan_details_fully_completed = models.CharField(
        max_length=20,
        choices=LoanDetailsFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    loan_details_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_source_of_lead_been_recorded = models.CharField(
        max_length=20,
        choices=HasSourceOfLeadBeenRecordedChoices.choices,
        null=True,
        blank=True,
    )
    has_source_of_lead_been_recorded_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    realistic_proximity_to_the_advisor = models.CharField(
        max_length=20,
        choices=RealisticProximityToTheAdvisorChoices.choices,
        null=True,
        blank=True,
    )
    realistic_proximity_to_the_advisor_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    personal_details = models.CharField(
        max_length=20, choices=PersonalDetailsChoices.choices, null=True, blank=True
    )
    personal_details_text = models.TextField(max_length=255, null=True, blank=True)
    retirement_age = models.CharField(
        choices=RetirementAgeChoices.choices, null=True, blank=True
    )
    retirement_age_text = models.TextField(max_length=255, null=True, blank=True)
    does_the_occupation_compared = models.CharField(
        max_length=20,
        choices=DoesTheOccupationComparedChoices.choices,
        null=True,
        blank=True,
    )
    does_the_occupation_compared_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    employment_details = models.CharField(
        max_length=20, choices=EmploymentDetailsChoices.choices, null=True, blank=True
    )
    employment_details_text = models.TextField(max_length=255, null=True, blank=True)
    has_due_diligence_been_completed = models.CharField(
        max_length=20,
        choices=HasDueDiligenceBeenCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_due_diligence_been_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_the_stated_income = models.CharField(
        max_length=20, choices=DoesTheStatedIncomeChoices.choices, null=True, blank=True
    )
    does_the_stated_income_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_the_stated_net_income = models.CharField(
        max_length=20,
        choices=DoesTheStatedNetIncomeChoices.choices,
        null=True,
        blank=True,
    )
    does_the_stated_net_income_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_the_client_in_an_occupation = models.CharField(
        max_length=20,
        choices=IsTheClientInAnOccupationChoices.choices,
        null=True,
        blank=True,
    )
    is_the_client_in_an_occupation_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_property_portfolio_fully_completed = models.CharField(
        max_length=20,
        choices=HasPropertyPortfolioFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_property_portfolio_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_proposed_property_details_fully_completed = models.CharField(
        max_length=20,
        choices=HasPropertyDetailsFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_proposed_property_details_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_your_needs_fully_completed = models.CharField(
        max_length=20,
        choices=HasYourNeedsFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_your_needs_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_repayment_vehicle_recorded = models.CharField(
        max_length=20,
        choices=HasRepaymentVehicleRecordedChoices.choices,
        null=True,
        blank=True,
    )
    has_repayment_vehicle_recorded_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    have_figures_been_input = models.CharField(
        max_length=20,
        choices=HaveFiguresBeenInputChoices.choices,
        null=True,
        blank=True,
    )
    have_figures_been_input_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_deposit_come_from_sale_of_property = models.CharField(
        max_length=20,
        choices=IsDepositComeFromSaleOfPropertyChoices.choices,
        null=True,
        blank=True,
    )
    is_deposit_come_from_sale_of_property_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_adviser_completed_calculator = models.CharField(
        max_length=20,
        choices=HasAdviserCompletedCalculatorChoices.choices,
        null=True,
        blank=True,
    )
    has_adviser_completed_calculator_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_accountant_solicitor_details_confirmed = models.CharField(
        max_length=20,
        choices=HasAccountantSolicitorDetailsBeenConfirmedChoices.choices,
        null=True,
        blank=True,
    )
    has_accountant_solicitor_details_confirmed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_credit_commitments_fully_completed = models.CharField(
        max_length=20,
        choices=HasCreditCommitmentsFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_credit_commitments_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_any_credit_commitments = models.CharField(
        max_length=20,
        choices=IsAnyCreditCommitmentsChoices.choices,
        null=True,
        blank=True,
    )
    is_any_credit_commitments_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_client_adverse_credit = models.CharField(
        max_length=20,
        choices=HasClientAdverseCreditChoices.choices,
        null=True,
        blank=True,
    )
    has_client_adverse_credit_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_budget_planner_been_completed = models.CharField(
        max_length=20,
        choices=HasBudgetPlannerBeenCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_budget_planner_been_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_all_direct_debits_been_recorded = models.CharField(
        max_length=20,
        choices=HasAllDirectDebitsBeenRecordedChoices.choices,
        null=True,
        blank=True,
    )
    has_all_direct_debits_been_recorded_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_adviser_sourced_mortgage_requirements = models.CharField(
        max_length=20,
        choices=HasAdviserSourcedMortgageRequirementsChoices.choices,
        null=True,
        blank=True,
    )
    has_adviser_sourced_mortgage_requirement_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_figures_stated_in_mortgage_requirements = models.CharField(
        max_length=20,
        choices=FiguresStatedInMortgageRequirementsChoices.choices,
        null=True,
        blank=True,
    )
    does_figures_stated_in_mortgage_requirements_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_results_stored_in_order_of_client_preference = models.CharField(
        max_length=20,
        choices=AreResultsStoredInOrderOfClientPreferenceChoices.choices,
        null=True,
        blank=True,
    )
    are_results_stored_in_order_of_client_preference_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_recommended_product_showing_evidence_research = models.CharField(
        max_length=20,
        choices=IsRecommendedProductShowingEvidenceResearchChoices.choices,
        null=True,
        blank=True,
    )
    is_recommended_product_showing_evidence_research_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_the_address_on_the_kfi_correct = models.CharField(
        max_length=20,
        choices=IsTheAddressOnTheKFICorrectChoices.choices,
        null=True,
        blank=True,
    )
    is_the_address_on_the_kfi_correct_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_figures_features_mortgage_requirements = models.CharField(
        max_length=20,
        choices=DoesFiguresFeaturesMortgageRequirementsChoices.choices,
        null=True,
        blank=True,
    )
    does_figures_features_mortgage_requirement_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_monthly_payment_fit_within_disposable_income = models.CharField(
        max_length=20,
        choices=DoesMonthlyPaymentFitWithinDisposableIncomeChoices.choices,
        null=True,
        blank=True,
    )
    does_monthly_payment_fit_within_disposable_income_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_fees_disclosed_correctly = models.CharField(
        max_length=20,
        choices=AreFeesDisclosedCorrectlyChoices.choices,
        null=True,
        blank=True,
    )
    are_fees_disclosed_correctly_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    lender_fees_added = models.CharField(
        max_length=20, choices=LenderFeesAddedChoices.choices, null=True, blank=True
    )
    lender_fees_added_text = models.TextField(max_length=255, null=True, blank=True)
    has_illustration_been_produced = models.CharField(
        max_length=20,
        choices=HasIllustrationBeenProducedChoices.choices,
        null=True,
        blank=True,
    )
    has_illustration_been_produced_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    interest_only = models.CharField(
        max_length=20, choices=InterestOnlyChoices.choices, null=True, blank=True
    )
    interest_only_text = models.TextField(max_length=255, null=True, blank=True)
    has_product_been_fully_completed = models.CharField(
        max_length=20,
        choices=HasProductBeenFullyCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_product_been_fully_completed_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    personal_details_match_the_factfind = models.CharField(
        max_length=20,
        choices=PersonalDetailsMatchTheFactfindChoices.choices,
        null=True,
        blank=True,
    )
    personal_details_match_the_factfind_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_employment_and_income_details_match = models.CharField(
        max_length=20,
        choices=DoesEmploymentIncomeDetailsMatchChoices.choices,
        null=True,
        blank=True,
    )
    does_employment_and_income_details_match_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_property_loan_details_match = models.CharField(
        max_length=20,
        choices=DoesPropertyLoanDetailsMatchChoices.choices,
        null=True,
        blank=True,
    )
    does_property_loan_details_match_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_mortgage_application_confirm = models.CharField(
        max_length=20,
        choices=DoesMortgageApplicationConfirmChoices.choices,
        null=True,
        blank=True,
    )
    does_mortgage_application_confirm_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_suitability_letter_been_generated = models.CharField(
        max_length=20,
        choices=HasSuitabilityLetterBeenGeneratedChoices.choices,
        null=True,
        blank=True,
    )
    has_suitability_letter_been_generated_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    post_application_changes = models.CharField(
        max_length=20,
        choices=PostApplicationChangesChoices.choices,
        null=True,
        blank=True,
    )
    post_application_changes_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_applicants_live_at_separate_addresses = models.CharField(
        max_length=20,
        choices=IsApplicantsLiveAtSeparateAddressesChoices.choices,
        null=True,
        blank=True,
    )
    is_applicants_live_at_separate_addresses_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    is_replacement_suitability_letter = models.CharField(
        max_length=20,
        choices=IsReplacementSuitabilityLetterChoices.choices,
        null=True,
        blank=True,
    )
    is_replacement_suitability_letter_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_reasons_for_mortgage_been_personalised = models.CharField(
        max_length=20,
        choices=HasReasonsForMortgageBeenPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_reasons_for_mortgage_been_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_meeting_discussion_been_personalised = models.CharField(
        max_length=20,
        choices=HasMeetingDiscussionBeenPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_meeting_discussion_been_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_circumstances_objectives_personalised = models.CharField(
        max_length=20,
        choices=HasCircumstancesObjectivesPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_circumstances_objectives_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_budget_affordability_been_personalised = models.CharField(
        max_length=20,
        choices=HasBudgetAffordabilityBeenPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_budget_affordability_been_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_new_mortgage_details_been_completed = models.CharField(
        max_length=20,
        choices=HasNewMortgageDetailsBeenCompletedChoices.choices,
        null=True,
        blank=True,
    )
    has_new_mortgage_details_been_complete_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_mortgage_section_one_personalised = models.CharField(
        max_length=20,
        choices=HasMortgageSectionOnePersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_mortgage_section_one_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_mortgage_section_two_personalised = models.CharField(
        max_length=20,
        choices=HasMortgageSectionTwoPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_mortgage_section_two_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_we_recommending_repayment_method = models.CharField(
        max_length=20,
        choices=AreWeRecommendingRepaymentMethodChoices.choices,
        null=True,
        blank=True,
    )
    are_we_recommending_repayment_method_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_we_recommending_mortgage_type = models.CharField(
        max_length=20,
        choices=AreWeRecommendingRepaymentTypeChoices.choices,
        null=True,
        blank=True,
    )
    are_we_recommending_mortgage_type_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_we_recommending_mortgage_term = models.CharField(
        max_length=20,
        choices=AreWeRecommendingRepaymentTermChoices.choices,
        null=True,
        blank=True,
    )
    are_we_recommending_mortgage_term_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_we_recommending_mortgage_lender = models.CharField(
        max_length=20,
        choices=AreWeRecommendingRepaymentLenderChoices.choices,
        null=True,
        blank=True,
    )
    are_we_recommending_mortgage_lender_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_we_recommending_mortgage_amount = models.CharField(
        max_length=20,
        choices=AreWeRecommendingRepaymentAmountChoices.choices,
        null=True,
        blank=True,
    )
    are_we_recommending_mortgage_amount_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_cost_and_fees_been_completed = models.CharField(
        max_length=20,
        choices=AreCostAndFeesBeenCompletedChoices.choices,
        null=True,
        blank=True,
    )
    are_cost_and_fees_been_complete_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    are_disadvantages_risks_been_selected = models.CharField(
        max_length=20,
        choices=AreDisadvantagesRisksBeenSelectedChoices.choices,
        null=True,
        blank=True,
    )
    are_disadvantages_risks_been_selected_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_adviser_personalised = models.CharField(
        max_length=20,
        choices=HasAdviserPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_adviser_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_adviser_included = models.CharField(
        max_length=20, choices=HasAdviserIncludedChoices.choices, null=True, blank=True
    )
    has_adviser_included_text = models.TextField(max_length=255, null=True, blank=True)
    has_protection_section_personalised = models.CharField(
        max_length=20,
        choices=HasProtectionSectionPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_protection_section_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_b_and_c_section_personalised = models.CharField(
        max_length=20,
        choices=HasBASectionPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_b_and_c_section_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    has_wills_section_personalised = models.CharField(
        max_length=20,
        choices=HasWillsSectionPersonalisedChoices.choices,
        null=True,
        blank=True,
    )
    has_wills_section_personalised_text = models.TextField(
        max_length=255, null=True, blank=True
    )
    does_recommended_product_match_your_needs_section = models.CharField(
        max_length=20,
        choices=DoesRecommendedProductMatchYourNeedsSectionChoices.choices,
        null=True,
        blank=True,
    )
    does_recommended_product_match_your_needs_section_text = models.TextField(
        max_length=255, null=True, blank=True
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.date_file_checked} {self.date_file_rechecked}"

# Client Servey Model
class ClientSurvey(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="client_servey")
    adviser_name = models.CharField(max_length=100)
    is_clarification_explanation_of_the_service_firm = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_timely_service_delivery = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_helpfulness_representative = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    the_firm_offices_reason = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_accuracy_information_provided = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_clarification_explanation_paid = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_raising_queries_relating_service = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_clarification_explanation_protection_review = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_understanding_of_financial_objectives = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_explanation_consideration_of_attitude_risk = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_explanation_consideration_capacity_loss_of_capital = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_explanation_adviser_product = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_interaction_adviser_professionals = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_suitable_advice_for_your_needs = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_ability_of_the_adviser_undue_pressure_commit = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_timing_deliver_review_by_adviser = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    the_broker_fee_paid_represents = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    explanation_broker_fees_including_refund_policy = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_receive_the_value_expected_broker_fee = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_any_other_documentation_provided_to_you = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_timing_arrangements_made_conduct_review_with_you = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null=True,
        blank=True,
    )
    is_frequency_communications_receive_from_firm = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null = True,
        blank=True,
    )
    is_relevance_communications_sent_to_the_firm = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null = True,
        blank=True,
    )
    is_raising_any_queries_on_communications = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null = True,
        blank=True,
    )
    is_overall_standard_communications_received_from_firm = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null = True,
        blank=True,
    )
    is_timely_manner_of_receiving_letter_confirming_recommendation = models.CharField(
        max_length=100,
        choices=ClientServeyChoices.choices,
        null = True,
        blank=True,
    )
    do_we_better_serve_next_time = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    have_any_further_comments_on_the_service_received = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    do_you_like_someone_to_contact_you = models.CharField(
        max_length=100,
        choices=DoYouLikeSomeoneToContactYouChoices.choices,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    client_survey = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.name} ({self.email})"


# Call all signals here.
post_save.connect(create_loan_details, sender=Case)
post_save.connect(create_applicant_details, sender=Case)
post_save.connect(create_applicant_details_for_joint_user, sender=JointUser)
post_save.connect(create_employment_details_for_lead, sender=Case)
post_save.connect(create_employment_details_for_joint_user, sender=JointUser)
post_save.connect(create_adverse_for_lead, sender=Case)
post_save.connect(create_adverse_for_joint_user, sender=JointUser)
post_save.connect(create_property_details, sender=Case)
post_save.connect(create_budget_planner, sender=Case)
post_save.connect(create_mortgage_needs, sender=Case)
post_save.connect(create_mortgage_features, sender=Case)
post_save.connect(create_mortgage_features_for_joint_user, sender=JointUser)
post_save.connect(create_suitability, sender=Case)
post_save.connect(create_compliance, sender=Case)
post_save.connect(create_client_survey, sender=Case)