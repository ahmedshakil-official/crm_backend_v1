from django.db import models
from django.utils.translation import gettext_lazy as _


class ApplicationTypeChoices(models.TextChoices):
    SELECT_APPLICATION_TYPE = "SELECT_APPLICATION_TYPE", _("Select Application Type")
    BUSINESS_LOAN = "BUSINESS_LOAN", _("Business Loan")
    BUY_TO_LET = "BUY_TO_LET", _("Buy to Let Mortgage")
    COMMERCIAL_MORTGAGE = "COMMERCIAL_MORTGAGE", _("Commercial Mortgage")
    HMO_MORTGAGE = "HMO_MORTGAGE", _("HMO Mortgage")
    RESIDENTIAL_MORTGAGE = "RESIDENTIAL_MORTGAGE", _("Residential Mortgage")
    SECOND_CHARGE_MORTGAGE = "SECOND_CHARGE_MORTGAGE", _("Second Charge Mortgage")


class LenderChoices(models.TextChoices):
    ACCORD_MORTGAGES = "ACCORD_MORTGAGES", _("Accord Mortgages")
    AHLI_UNITED_BANK = "AHLI_UNITED_BANK", _("Ahli United Bank")
    AL_RAYAN_BANK = "AL_RAYAN_BANK", _("Al Rayan Bank")
    ALDERMORE_MORTGAGES = "ALDERMORE_MORTGAGES", _("Aldermore Mortgages")
    AMICUS_PLC = "AMICUS_PLC", _("Amicus PLC")
    ASSETZ_CAPITAL = "ASSETZ_CAPITAL", _("Assetz Capital")
    ATOM_BANK = "ATOM_BANK", _("Atom Bank")
    AVIVA_EQUITY_RELEASE = "AVIVA_EQUITY_RELEASE", _("Aviva Equity Release")
    AXIS_BANK = "AXIS_BANK", _("Axis Bank")
    BANK_AND_CLIENTS_PLC = "BANK_AND_CLIENTS_PLC", _("Bank & Clients PLC")
    BANK_OF_CHINA = "BANK_OF_CHINA", _("Bank of China")
    BANK_OF_CYPRUS_UK = "BANK_OF_CYPRUS_UK", _("Bank of Cyprus UK")
    BANK_OF_IRELAND = "BANK_OF_IRELAND", _("Bank of Ireland")
    BARCLAYS = "BARCLAYS", _("Barclays")
    BARCLAYS_COMMERCIAL = "BARCLAYS_COMMERCIAL", _("Barclays Commercial")
    BATH_BUILDING_SOCIETY = "BATH_BUILDING_SOCIETY", _("Bath Building Society")
    BEVERLEY_BUILDING_SOCIETY = "BEVERLEY_BUILDING_SOCIETY", _(
        "Beverley Building Society"
    )
    BLUESTONE_MORTGAGES = "BLUESTONE_MORTGAGES", _("Bluestone Mortgages")
    BLUEZEST = "BLUEZEST", _("BlueZest")
    BM_SOLUTIONS = "BM_SOLUTIONS", _("BM Solutions")
    BOOST_CAPITAL = "BOOST_CAPITAL", _("Boost Capital")
    BRIDGEWATER_EQUITY_RELEASE = "BRIDGEWATER_EQUITY_RELEASE", _(
        "Bridgewater Equity Release"
    )
    BUCKINGHAMSHIRE_BUILDING_SOCIETY = "BUCKINGHAMSHIRE_BUILDING_SOCIETY", _(
        "Buckinghamshire Building Society"
    )
    CAMBRIDGE_AND_COUNTIES_BANK = "CAMBRIDGE_AND_COUNTIES_BANK", _(
        "Cambridge and Counties Bank"
    )
    CAMBRIDGE_BUILDING_SOCIETY = "CAMBRIDGE_BUILDING_SOCIETY", _(
        "Cambridge Building Society"
    )
    CENTRAL_TRUST = "CENTRAL_TRUST", _("Central Trust")
    CHARTERBANK = "CHARTERBANK", _("Charterbank")
    CHL_MORTGAGES = "CHL_MORTGAGES", _("CHL Mortgages")
    CHORLEY_DISTRICT_BUILDING_SOCIETY = "CHORLEY_DISTRICT_BUILDING_SOCIETY", _(
        "Chorley & District Building Society"
    )
    CLEARLY_LOANS = "CLEARLY_LOANS", _("Clearly Loans")
    COUTTS = "COUTTS", _("Coutts")
    COVENTRY_BUILDING_SOCIETY = "COVENTRY_BUILDING_SOCIETY", _(
        "Coventry Building Society"
    )
    CROWN_EQUITY_RELEASE = "CROWN_EQUITY_RELEASE", _("Crown Equity Release")
    CUMBERLAND_BUILDING_SOCIETY = "CUMBERLAND_BUILDING_SOCIETY", _(
        "Cumberland Building Society"
    )
    DANSKE_BANK = "DANSKE_BANK", _("Danske Bank")
    DARLINGTON_BUILDING_SOCIETY = "DARLINGTON_BUILDING_SOCIETY", _(
        "Darlington Building Society"
    )
    DIGITAL_MORTGAGES = "DIGITAL_MORTGAGES", _("Digital Mortgages")
    DUDLEY_BUILDING_SOCIETY = "DUDLEY_BUILDING_SOCIETY", _("Dudley Building Society")
    EARL_SHILTON_BUILDING_SOCIETY = "EARL_SHILTON_BUILDING_SOCIETY", _(
        "Earl Shilton Building Society"
    )
    ECOLOGY_BUILDING_SOCIETY = "ECOLOGY_BUILDING_SOCIETY", _("Ecology Building Society")
    EQUIFINANCE = "EQUIFINANCE", _("Equifinance")
    FAMILY_BUILDING_SOCIETY = "FAMILY_BUILDING_SOCIETY", _("Family Building Society")
    FINSEC = "FINSEC", _("FinSec")
    FIRST_TRUST_BANK = "FIRST_TRUST_BANK", _("First Trust Bank")
    FLEET_MORTGAGES = "FLEET_MORTGAGES", _("Fleet Mortgages")
    FOUNDATION_HOME_LOANS = "FOUNDATION_HOME_LOANS", _("Foundation Home Loans")
    FURNESS_BUILDING_SOCIETY = "FURNESS_BUILDING_SOCIETY", _("Furness Building Society")
    GATEHOUSE_BANK = "GATEHOUSE_BANK", _("Gatehouse Bank")
    GENERATION_HOME = "GENERATION_HOME", _("Generation Home")
    GODIVA_MORTGAGES = "GODIVA_MORTGAGES", _("Godiva Mortgages")
    HALIFAX = "HALIFAX", _("Halifax")
    HAMPSHIRE_TRUST_BANK = "HAMPSHIRE_TRUST_BANK", _("Hampshire Trust Bank")
    HANDELSBANKEN = "HANDELSBANKEN", _("Handelsbanken")
    HANLEY_ECONOMIC_BUILDING_SOCIETY = "HANLEY_ECONOMIC_BUILDING_SOCIETY", _(
        "Hanley Economic Building Society"
    )
    HARPDEN_BUILDING_SOCIETY = "HARPDEN_BUILDING_SOCIETY", _(
        "Harpenden Building Society"
    )
    HSBC = "HSBC", _("HSBC")
    ICICI_BANK = "ICICI_BANK", _("ICICI Bank")
    INTERBAY_COMMERCIAL = "INTERBAY_COMMERCIAL", _("Interbay Commercial")
    INVESTEC = "INVESTEC", _("Investec")
    IPSWICH_BUILDING_SOCIETY = "IPSWICH_BUILDING_SOCIETY", _("Ipswich Building Society")
    JUST_RETIREMENT_SOLUTIONS = "JUST_RETIREMENT_SOLUTIONS", _(
        "Just Retirement Solutions"
    )
    KENSINGTON_MORTGAGES = "KENSINGTON_MORTGAGES", _("Kensington Mortgages")
    KENT_RELIANCE = "KENT_RELIANCE", _("Kent Reliance")
    KEYSTONE_PROPERTY_FINANCE = "KEYSTONE_PROPERTY_FINANCE", _(
        "Keystone Property Finance"
    )
    LEEDS_BUILDING_SOCIETY = "LEEDS_BUILDING_SOCIETY", _("Leeds Building Society")
    LEEK_UNITED_BUILDING_SOCIETY = "LEEK_UNITED_BUILDING_SOCIETY", _(
        "Leek United Building Society"
    )
    METRO_BANK = "METRO_BANK", _("Metro Bank")
    MONMOUTHSHIRE_BUILDING_SOCIETY = "MONMOUTHSHIRE_BUILDING_SOCIETY", _(
        "Monmouthshire Building Society"
    )
    NATIONWIDE = "NATIONWIDE", _("Nationwide")
    NATWEST = "NATWEST", _("NatWest")
    NOTTINGHAM_BUILDING_SOCIETY = "NOTTINGHAM_BUILDING_SOCIETY", _(
        "Nottingham Building Society"
    )
    PARAGON_MORTGAGES = "PARAGON_MORTGAGES", _("Paragon Mortgages")
    PEPPER_MONEY = "PEPPER_MONEY", _("Pepper Money")
    POST_OFFICE_MORTGAGES = "POST_OFFICE_MORTGAGES", _("Post Office Mortgages")
    PRINCIPALITY_BUILDING_SOCIETY = "PRINCIPALITY_BUILDING_SOCIETY", _(
        "Principality Building Society"
    )
    SANTANDER = "SANTANDER", _("Santander")
    SKIPTON_BUILDING_SOCIETY = "SKIPTON_BUILDING_SOCIETY", _("Skipton Building Society")
    TSB = "TSB", _("TSB")
    ULSTER_BANK = "ULSTER_BANK", _("Ulster Bank")
    UNKNOWN = "UNKNOWN", _("Unknown")
    UNKNOWN_DEFAULT = "UNKNOWN_DEFAULT", _("Unknown (Default)")
    VIDA_HOMELOANS = "VIDA_HOMELOANS", _("Vida Homeloans")
    WEST_BROMWICH_BUILDING_SOCIETY = "WEST_BROMWICH_BUILDING_SOCIETY", _(
        "West Bromwich Building Society"
    )
    WEST_ONE_LOANS = "WEST_ONE_LOANS", _("West One Loans")


class MortgageTypeChoices(models.TextChoices):
    PURCHASE = "PURCHASE", _("Purchase")
    REMORTGAGE = "REMORTGAGE", _("Remortgage")
    SECURED_LOAN = "SECURED_LOAN", _("Secured Loan")
    FURTHER_ADVANCE = "FURTHER_ADVANCE", _("Further Advance")
    PRODUCT_TRANSFER = "PRODUCT_TRANSFER", _("Product Transfer")
    OTHER = "OTHER", _("Other")
    UNSECURED = "UNSECURED", _("Unsecured")
    INVOICE_DISCOUNTING = "INVOICE_DISCOUNTING", _("Invoice Discounting")
    ASSET_FINANCE = "ASSET_FINANCE", _("Asset Finance")


class LoanPurposeChoices(models.TextChoices):
    PURCHASE = "PURCHASE", _("Purchase")
    LIKE_FOR_LIKE_REMORTGAGE = "LIKE_FOR_LIKE_REMORTGAGE", _("Like for Like Remortgage")
    BUSINESS_PURPOSES = "BUSINESS_PURPOSES", _("Business Purposes")
    DEBT_CONSOLIDATION = "DEBT_CONSOLIDATION", _("Debt Consolidation")
    DIVORCE_SETTLEMENT = "DIVORCE_SETTLEMENT", _("Divorce Settlement")
    HOLIDAYS_CARS = "HOLIDAYS_CARS", _("Holidays/Cars")
    HOME_IMPROVEMENTS = "HOME_IMPROVEMENTS", _("Home Improvements")
    OTHER_PROPERTY_PURCHASE = "OTHER_PROPERTY_PURCHASE", _("Other Property Purchase")
    SCHOOL_FEES = "SCHOOL_FEES", _("School Fees")
    RATE_SWITCH = "RATE_SWITCH", _("Rate Switch (switch to better rate)")
    TAX_BILL = "TAX_BILL", _("Tax Bill")


class BorrowerTypeChoices(models.TextChoices):
    HOMEMOVER = "HOMEMOVER", _("Homemover")
    FIRST_TIME_BUYER = "FIRST_TIME_BUYER", _("First Time Buyer")
    RE_MORTGAGE = "RE_MORTGAGE", _("Re-Mortgage")
    CAPITAL_RAISE = "CAPITAL_RAISE", _("Capital Raise")
    HELP_TO_BUY = "HELP_TO_BUY", _("Help to Buy")
    SHARED_OWNERSHIP = "SHARED_OWNERSHIP", _("Shared Ownership")
    RIGHT_TO_BUY = "RIGHT_TO_BUY", _("Right to Buy")
    LATER_LIFE_LENDING = "LATER_LIFE_LENDING", _("Later Life Lending")
    EQUITY_RELEASE = "EQUITY_RELEASE", _("Equity Release")
    BUY_TO_LET = "BUY_TO_LET", _("Buy to Let")
    LET_TO_BUY = "LET_TO_BUY", _("Let to Buy")
    FIRST_TIME_LANDLORD = "FIRST_TIME_LANDLORD", _("First Time Landlord")
    PORTFOLIO_LANDLORD = "PORTFOLIO_LANDLORD", _("Portfolio Landlord")
    SHARED_EQUITY = "SHARED_EQUITY", _("Shared Equity")
    ISLAMIC_MORTGAGE = "ISLAMIC_MORTGAGE", _("Islamic Mortgage")


class RepaymentMethodChoices(models.TextChoices):
    CAPITAL_AND_INTEREST = "CAPITAL_AND_INTEREST", _("Capital and Interest")
    INTEREST_ONLY = "INTEREST_ONLY", _("Interest Only")
    PART_AND_PART = "PART_AND_PART", _("Part And Part")


class RepaymentVehicleChoices(models.TextChoices):
    ENDOWMENT = "ENDOWMENT", _("Endowment")
    INDIVIDUAL_SAVINGS_ACCOUNT = "INDIVIDUAL_SAVINGS_ACCOUNT", _(
        "Individual Savings Account"
    )
    PENSION = "PENSION", _("Pension")
    SALE_OF_MORTGAGED_PROPERTY = "SALE_OF_MORTGAGED_PROPERTY", _(
        "Sale of Mortgaged Property"
    )
    SALE_OF_OTHER_PROPERTY = "SALE_OF_OTHER_PROPERTY", _("Sale of Other Property")
    INHERITANCE = "INHERITANCE", _("Inheritance")
    MORTGAGE_LINKED_INVESTMENT = "MORTGAGE_LINKED_INVESTMENT", _(
        "Mortgage-Linked Investment"
    )
    REVERT_TO_CAPITAL_REPAYMENT = "REVERT_TO_CAPITAL_REPAYMENT", _(
        "Revert to Capital Repayment"
    )
    SALE_OF_NON_PROPERTY_ASSETS = "SALE_OF_NON_PROPERTY_ASSETS", _(
        "Sale of non-Property Assets"
    )
    OTHER = "OTHER", _("Other")


class InterestRateTypeChoices(models.TextChoices):
    FIXED = "FIXED", _("Fixed")
    VARIABLE = "VARIABLE", _("Variable")
    TRACKER = "TRACKER", _("Tracker")
    LIBOR_LINKED = "LIBOR_LINKED", _("Libor Linked")
    DISCOUNT = "DISCOUNT", _("Discount")
    CAPPED = "CAPPED", _("Capped")
    ALL = "ALL", _("All")


class ProductTermChoices(models.TextChoices):
    ONE_YEAR = "ONE_YEAR", _("1 Year")
    TWO_YEARS = "TWO_YEARS", _("2 Years")
    THREE_YEARS = "THREE_YEARS", _("3 Years")
    FOUR_YEARS = "FOUR_YEARS", _("4 Years")
    FIVE_PLUS_YEARS = "FIVE_PLUS_YEARS", _("5+ Years")
    FULL_TERM = "FULL_TERM", _("Full Term")


class AdviceLevelChoices(models.TextChoices):
    ADVISING = "ADVISING", _("Advising")
    EXECUTION_ONLY = "EXECUTION_ONLY", _("Execution Only")


class IntroductionTypeChoices(models.TextChoices):
    DIRECT = "DIRECT", _("Direct")
    RDI = "RDI", _("RDI")


class IntroducerPaymentTermsChoices(models.TextChoices):
    NOT_APPLICABLE = "NOT_APPLICABLE", _("Not Applicable")
    ON_APPLICATION = "ON_APPLICATION", _("On Application")
    ON_OFFER = "ON_OFFER", _("On Offer")
    ON_COMPLETION = "ON_COMPLETION", _("On Completion")


class LeadSourceChoices(models.TextChoices):
    FACEBOOK = "FACEBOOK", _("Facebook")
    ESTATE_AGENTS = "ESTATE_AGENTS", _("Estate Agents")
    TV3 = "TV3", _("TV3")
    FAMILY = "FAMILY", _("Family")
    FRIENDS = "FRIENDS", _("Friends")
    REFERRALS = "REFERRALS", _("Referrals")
    WEBSITE = "WEBSITE", _("Website")


class SaleTypeChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    FACE_TO_FACE = "FACE_TO_FACE", _("Face to Face")
    TELEPHONE = "TELEPHONE", _("Telephone")
    INTERNET = "INTERNET", _("Internet")
    OTHER = "OTHER", _("Other")


class CurrentLenderChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    ACCORD_MORTGAGES = "ACCORD_MORTGAGES", _("Accord Mortgages")
    AHLI_UNITED_BANK = "AHLI_UNITED_BANK", _("Ahli United Bank")
    AL_RAYAN_BANK = "AL_RAYAN_BANK", _("Al Rayan Bank")
    ALDERMORE_MORTGAGES = "ALDERMORE_MORTGAGES", _("Aldermore Mortgages")
    AMICUS_PLC = "AMICUS_PLC", _("Amicus PLC")
    ASSETZ_CAPITAL = "ASSETZ_CAPITAL", _("Assetz Capital")
    ATOM_BANK = "ATOM_BANK", _("Atom Bank")
    AVIVA_EQUITY_RELEASE = "AVIVA_EQUITY_RELEASE", _("Aviva Equity Release")
    AXIS_BANK = "AXIS_BANK", _("Axis Bank")
    BANK_AND_CLIENTS_PLC = "BANK_AND_CLIENTS_PLC", _("Bank & Clients PLC")
    BANK_OF_CHINA = "BANK_OF_CHINA", _("Bank of China")
    BANK_OF_CYPRUS_UK = "BANK_OF_CYPRUS_UK", _("Bank of Cyprus UK")
    BANK_OF_IRELAND = "BANK_OF_IRELAND", _("Bank of Ireland")
    BARCLAYS = "BARCLAYS", _("Barclays")
    BARCLAYS_COMMERCIAL = "BARCLAYS_COMMERCIAL", _("Barclays Commercial")
    BATH_BUILDING_SOCIETY = "BATH_BUILDING_SOCIETY", _("Bath Building Society")
    BEVERLEY_BUILDING_SOCIETY = "BEVERLEY_BUILDING_SOCIETY", _(
        "Beverley Building Society"
    )
    BLUESTONE_MORTGAGES = "BLUESTONE_MORTGAGES", _("Bluestone Mortgages")
    BLUEZEST = "BLUEZEST", _("BlueZest")
    BM_SOLUTIONS = "BM_SOLUTIONS", _("BM Solutions")
    BOOST_CAPITAL = "BOOST_CAPITAL", _("Boost Capital")
    BRIDGEWATER_EQUITY_RELEASE = "BRIDGEWATER_EQUITY_RELEASE", _(
        "Bridgewater Equity Release"
    )
    BUCKINGHAMSHIRE_BUILDING_SOCIETY = "BUCKINGHAMSHIRE_BUILDING_SOCIETY", _(
        "Buckinghamshire Building Society"
    )
    CAMBRIDGE_AND_COUNTIES_BANK = "CAMBRIDGE_AND_COUNTIES_BANK", _(
        "Cambridge and Counties Bank"
    )
    CAMBRIDGE_BUILDING_SOCIETY = "CAMBRIDGE_BUILDING_SOCIETY", _(
        "Cambridge Building Society"
    )
    CENTRAL_TRUST = "CENTRAL_TRUST", _("Central Trust")
    CHARTERBANK = "CHARTERBANK", _("Charterbank")
    CHL_MORTGAGES = "CHL_MORTGAGES", _("CHL Mortgages")
    CHORLEY_AND_DISTRICT_BUILDING_SOCIETY = "CHORLEY_AND_DISTRICT_BUILDING_SOCIETY", _(
        "Chorley & District Building Society"
    )
    CLEARLY_LOANS = "CLEARLY_LOANS", _("Clearly Loans")
    CLYDESDALE_BANK = "CLYDESDALE_BANK", _("Clydesdale Bank")
    COUTTS = "COUTTS", _("Coutts")
    COVENTRY_BUILDING_SOCIETY = "COVENTRY_BUILDING_SOCIETY", _(
        "Coventry Building Society"
    )
    CROWN_EQUITY_RELEASE = "CROWN_EQUITY_RELEASE", _("Crown Equity Release")
    CUMBERLAND_BUILDING_SOCIETY = "CUMBERLAND_BUILDING_SOCIETY", _(
        "Cumberland Building Society"
    )
    DANSKE_BANK = "DANSKE_BANK", _("Danske Bank")
    DARLINGTON_BUILDING_SOCIETY = "DARLINGTON_BUILDING_SOCIETY", _(
        "Darlington Building Society"
    )
    DIGITAL_MORTGAGES = "DIGITAL_MORTGAGES", _("Digital Mortgages")
    DUDLEY_BUILDING_SOCIETY = "DUDLEY_BUILDING_SOCIETY", _("Dudley Building Society")
    EARL_SHILTON_BUILDING_SOCIETY = "EARL_SHILTON_BUILDING_SOCIETY", _(
        "Earl Shilton Building Society"
    )
    ECOLOGY_BUILDING_SOCIETY = "ECOLOGY_BUILDING_SOCIETY", _("Ecology Building Society")
    EQUIFINANCE = "EQUIFINANCE", _("Equifinance")
    FAMILY_BUILDING_SOCIETY = "FAMILY_BUILDING_SOCIETY", _("Family Building Society")
    FINSEC = "FINSEC", _("FinSec")
    FIRST_TRUST_BANK = "FIRST_TRUST_BANK", _("First Trust Bank")
    UNKNOWN_DEFAULT = "UNKNOWN_DEFAULT", _("Unknown (Default)")


class TitleChoices(models.TextChoices):
    MR = "MR", _("Mr")
    MRS = "MRS", _("Mrs")
    MS = "MS", _("Ms")
    MISS = "MISS", _("Miss")


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")


class MaritalStatusChoices(models.TextChoices):
    SINGLE = "SINGLE", _("Single")
    MARRIED = "MARRIED", _("Married")
    DIVORCED = "DIVORCED", _("Divorced")
    SEPARATED = "SEPARATED", _("Separated")
    WIDOW = "WIDOW", _("Widow")
    WIDOWER = "WIDOWER", _("Widower")
    CO_HABITING = "CO_HABITING", _("Co-Habiting")
    CIVIL_PARTNER = "CIVIL_PARTNER", _("Civil Partner")
    RELIGIOUSLY_MARRIED = "RELIGIOUSLY_MARRIED", _("Religiously Married")


class MarketingPreferencesChoices(models.TextChoices):
    EMAIL = "EMAIL", _("Email")
    TELEPHONE = "TELEPHONE", _("Telephone")
    SMS = "SMS", _("SMS")
    POST = "POST", _("Post")
    NO_COMMUNICATION = "NO_COMMUNICATION", _("No Communication")


class ResidentialStatus(models.TextChoices):
    OWNER = "OWNER", _("Owner")
    RENTING_PRIVATE = "RENTING_PRIVATE", _("Renting - private")
    RENTING_LOCAL_AUTHORITY = "RENTING_LOCAL_AUTHORITY", _("Renting - Local Authority")
    TIED_ACCOMMODATION = "TIED_ACCOMMODATION", _("Tied Accommodation")
    LIVING_WITH_PARENTS = "LIVING_WITH_PARENTS", _("Living with Parents")
    LIVING_WITH_FRIENDS_FAMILY = "LIVING_WITH_FRIENDS_FAMILY", _(
        "Living with Friends/Family"
    )


class MortgageType(models.TextChoices):
    SECURED_LOAN = "SECURED_LOAN", _("Secured Loan (Applicant Commitments)")
    SECOND_HOME = "SECOND_HOME", _("Second Home (Applicant Commitments)")
    HOLIDAY_HOME = "HOLIDAY_HOME", _("Holiday Home (Applicant Commitments)")
    BUY_TO_LET = "BUY_TO_LET", _("Buy to Let (Applicant Mortgage Details)")
    HOLIDAY_LET = "HOLIDAY_LET", _("Holiday Let (Applicant Mortgage Details)")
    COMMERCIAL_INVESTMENT = "COMMERCIAL_INVESTMENT", _(
        "Commercial Investment (Applicant Mortgage Details)"
    )


class RepaymentType(models.TextChoices):
    CAPITAL_INTEREST = "CAPITAL_INTEREST", _("Capital and Interest")
    INTEREST_ONLY = "INTEREST_ONLY", _("Interest Only")
    PART_AND_PART = "PART_AND_PART", _("Part And Part")
    SERVICED = "SERVICED", _("Serviced")
    ROLLED_UP = "ROLLED_UP", _("Rolled Up")
    RETAINED = "RETAINED", _("Retained")
    OTHER = "OTHER", _("Other")


class InterestType(models.TextChoices):
    FIXED = "FIXED", _("Fixed")
    VARIABLE = "VARIABLE", _("Variable")
    TRACKER = "TRACKER", _("Tracker")
    DISCOUNT = "DISCOUNT", _("Discount")
    CAPPED = "CAPPED", _("Capped")
    SVR = "SVR", _("SVR")
    OFFSET = "OFFSET", _("Offset")
    LIFETIME = "LIFETIME", _("Lifetime")
    OTHER = "OTHER", _("Other")


class ERCCompletionStatus(models.TextChoices):
    NA = "NA", _("N/A")
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class PropertyType(models.TextChoices):
    HOUSE = "HOUSE", _("House")
    FLAT = "FLAT", _("Flat")
    MAISONETTE = "MAISONETTE", _("Maisonette")
    BUNGALOW = "BUNGALOW", _("Bungalow")
    WAREHOUSE = "WAREHOUSE", _("Warehouse")
    LAND = "LAND", _("Land")
    COMMERCIAL = "COMMERCIAL", _("Commercial")
    SEMI_COMMERCIAL = "SEMI_COMMERCIAL", _("Semi-Commercial")
    MULTI_UNIT_BLOCK = "MULTI_UNIT_BLOCK", _("Multi-Unit Block (MUB)")
    HMO = "HMO", _("HMO")


class TenureType(models.TextChoices):
    FREEHOLD = "FREEHOLD", _("Freehold")
    LEASEHOLD = "LEASEHOLD", _("Leasehold")
    COMMONHOLD = "COMMONHOLD", _("Commonhold")
    FEUDAL = "FEUDAL", _("Feudal")


class CompanyType(models.TextChoices):
    PRIVATE_LIMITED = "PRIVATE_LIMITED", _("Private Limited Company")
    PUBLIC_LIMITED = "PUBLIC_LIMITED", _("Public Limited Company")
    SOLE_TRADER = "SOLE_TRADER", _("Sole Trader")
    PARTNERSHIP = "PARTNERSHIP", _("Partnership")
    LIMITED_LIABILITY_PARTNERSHIP = "LIMITED_LIABILITY_PARTNERSHIP", _(
        "Limited Liability Partnership"
    )
    OTHER = "OTHER", _("Other")


class RoleType(models.TextChoices):
    DIRECTOR = "DIRECTOR", _("Director")
    SHAREHOLDER = "SHAREHOLDER", _("Share Holder")
    BOTH = "BOTH", _("Both")


class EmploymentStatus(models.TextChoices):
    EMPLOYED = "EMPLOYED", _("Employed")
    SELF_EMPLOYED = "SELF_EMPLOYED", _("Self Employed")
    RETIRED = "RETIRED", _("Retired")
    OTHER = "OTHER", _("Other")
    UNEMPLOYED = "UNEMPLOYED", _("Unemployed")
    HOUSEPERSON = "HOUSEPERSON", _("Houseperson")
    CONTRACTOR = "CONTRACTOR", _("Contractor")


class EmploymentType(models.TextChoices):
    PERMANENT = "PERMANENT", _("Permanent")
    CONTRACT = "CONTRACT", _("Contract")
    TEMPORARY = "TEMPORARY", _("Temporary")


class FrequencyChoice(models.TextChoices):
    NEVER = "NEVER", _("Never")
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    BI_WEEKLY = "BI_WEEKLY", _("Bi Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    BI_MONTHLY = "BI_MONTHLY", _("Bi Monthly")
    QUARTERLY = "QUARTERLY", _("Quarterly")
    BI_ANNUALLY = "BI_ANNUALLY", _("Bi Annually")
    ANNUALLY = "ANNUALLY", _("Annually")


class CompanyTypeChoices(models.TextChoices):
    SOLE_TRADER = "SOLE_TRADER", _("Sole Trader")
    LIMITED_COMPANY = "LIMITED_COMPANY", _("Limited Company")
    PARTNERSHIP = "PARTNERSHIP", _("Partnership")
    LLP = "LLP", _("LLP")
    INDIVIDUAL = "INDIVIDUAL", _("Individual")


class CommitmentTypeChoices(models.TextChoices):
    CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
    STORE_CARD = "STORE_CARD", _("Store Card")
    LOAN = "LOAN", _("Loan")
    HP = "HP", _("HP")
    OVERDRAFT = "OVERDRAFT", _("Overdraft")
    STUDENT_LOAN = "STUDENT_LOAN", _("Student Loan")
    MAINTENANCE = "MAINTENANCE", _("Maintenance")
    LEASE = "LEASE", _("Lease")
    UNSECURED = "UNSECURED", _("Unsecured")
    MORTGAGE_RENT = "MORTGAGE_RENT", _("Mortgage/Rent")
    PUBLIC_UTILITY = "PUBLIC_UTILITY", _("Public Utility")
    COMMUNICATIONS = "COMMUNICATIONS", _("Communications")
    INSURANCE = "INSURANCE", _("Insurance")
    SECURED = "SECURED", _("Secured")
    PCP = "PCP", _("PCP")
    MAIL_ORDER = "MAIL_ORDER", _("Mail Order")
    CHILDCARE = "CHILDCARE", _("Childcare")
    CAR_FINANCE = "CAR_FINANCE", _("Car Finance")
    BUY_NOW_PAY_LATER = "BUY_NOW_PAY_LATER", _("Buy Now Pay Later (BNPL)")
    CREDIT_COMMITMENT = "CREDIT_COMMITMENT", _("Credit Commitment")
    DMP = "DMP", _("DMP")
    UNKNOWN = "UNKNOWN", _("Unknown")


class PlanChoices(models.TextChoices):
    DIRECT = "DIRECT", _("Direct")
    THIRD_PARTY = "THIRD_PARTY", _("Third Party")


class RateTypeChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    FIXED = "FIXED", _("Fixed")
    VARIABLE = "VARIABLE", _("Variable")
    TRACKER = "TRACKER", _("Tracker")
    LIBOR_LINKED = "LIBOR_LINKED", _("Libor Linked")
    DISCOUNT = "DISCOUNT", _("Discount")
    CAPPED = "CAPPED", _("Capped")
    ALL = "ALL", _("All")
    SVR = "SVR", _("SVR")
    OFFSET = "OFFSET", _("Offset")
    LIFETIME = "LIFETIME", _("Lifetime")
    OTHER = "OTHER", _("Other")


class EPCRatingChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    A = "A", _("A")
    B = "B", _("B")
    C = "C", _("C")
    D = "D", _("D")
    E = "E", _("E")
    F = "F", _("F")
    G = "G", _("G")


class UserTypeChoices(models.TextChoices):
    ACCOUNTANT = "ACCOUNTANT", _("Accountant")
    SOLICITOR = "SOLICITOR", _("Solicitor")


class PolicyTypeChoices(models.TextChoices):
    LIFE_ASSURANCE_LEVEL = "LIFE_ASSURANCE_LEVEL", _("Life Assurance Level")
    LIFE_ASSURANCE_DECREASING = "LIFE_ASSURANCE_DECREASING", _(
        "Life Assurance Decreasing"
    )
    CRITICAL_ILLNESS_COVER_LEVEL = (
        "CRITICAL_ILLNESS_COVER_LEVEL",
        _("Critical Illness Cover Level"),
    )
    CRITICAL_ILLNESS_COVER_DECREASING = (
        "CRITICAL_ILLNESS_COVER_DECREASING",
        _("Critical Illness Cover Decreasing"),
    )
    MORTGAGE_PAYMENT_PROTECTION = "MORTGAGE_PAYMENT_PROTECTION", _(
        "Mortgage Payment Protection"
    )
    BUILDINGS_AND_CONTENTS = "BUILDINGS_AND_CONTENTS", _("Buildings And Contents")
    PRIVATE_PENSION = "PRIVATE_PENSION", _("Private Pension")
    DEATH_IN_SERVICE_BENEFIT = "DEATH_IN_SERVICE_BENEFIT", _("Death In Service Benefit")
    OTHER = "OTHER", _("Other")


class PremiumPaymentChoices(models.TextChoices):
    MONTHLY = "MONTHLY", _("Monthly")
    ANNUALLY = "ANNUALLY", _("Annually")


class InTrustChoices(models.TextChoices):
    NA = "NA", _("N/A")
    YES = "YES", _("Yes")
    NO = "NO", _("No")
    CLIENT_TO_ASCERTAIN = "CLIENT_TO_ASCERTAIN", _("Client To Ascertain")


class GuaranteedReviewableChoices(models.TextChoices):
    NA = "NA", _("N/A")
    GUARANTEED = "GUARANTEED", _("Guaranteed")
    REVIEWABLE = "REVIEWABLE", _("Reviewable")
    CLIENT_TO_ASCERTAIN_AGE = "CLIENT_TO_ASCERTAIN_AGE", _("Client To Ascertain")
    COSTED = "COSTED", _("Costed")


class PolicyCancellationChoices(models.TextChoices):
    NOT_VALUES_YET = "NOT_VALUES_YET", _("Not Values Yet")


class TasksNotesChoices(models.TextChoices):
    NOTE = "NOTE", _("Note")
    TASK = "TASK", _("Task")


class CategoryChoices(models.TextChoices):
    UNCATEGORISED = "UNCATEGORISED", _("Uncategorised")
    EMAIL_CORRESPONDENCE = "EMAIL_CORRESPONDENCE", _("Email Correspondence")
    TELEPHONE_CONVERSATION = "TELEPHONE_CONVERSATION", _("Telephone Conversation")
    LENDER_CORRESPONDENCE = "LENDER_CORRESPONDENCE", _("Lender Correspondence")
    SOLICITOR_CORRESPONDENCE = "SOLICITOR_CORRESPONDENCE", _("Solicitor Correspondence")
    COMPLIANCE_CORRESPONDENCE = "COMPLIANCE_CORRESPONDENCE", _(
        "Compliance Correspondence"
    )


class TaskPriorityChoices(models.TextChoices):
    LOW = "LOW", _("Low")
    NORMAL = "NORMAL", _("Normal")
    HIGH = "HIGH", _("High")
    URGENT = "URGENT", _("Urgent")


class InitialRateTypeChoices(models.TextChoices):
    PLEASE_SELECT_A_INITIAL_RATE_TYPE = "PLEASE_SELECT_A_INITIAL_RATE_TYPE", _(
        "Please Select A Initial Rate Type"
    )
    FIXED = "FIXED", _("Fixed")
    VARIABLE = "VARIABLE", _("Variable")
    TRACKER = "TRACKER", _("Tracker")
    DISCOUNTED = "DISCOUNTED", _("Discounted")
    ALL = "ALL", _("All")


class InitialRatePeriodTypeChoices(models.TextChoices):
    PLEASE_SELECT_A_INITIAL_RATE_PERIOD_TYPE = (
        "PLEASE_SELECT_A_INITIAL_RATE_PERIOD_TYPE",
        _("Please Select A Initial Rate Period Type"),
    )
    MONTHS = "MONTHS", _("Months")
    FIXED_DATE = "FIXED_DATE", _("Fixed Date")
    END_OF_MORTGAGE_TERM = "END_OF_MORTGAGE_TERM", _("End of Mortgage Term")


class ProductClassChoices(models.TextChoices):
    PLEASE_SELECT_A_PRODUCT_CLASS = "PLEASE_SELECT_A_PRODUCT_CLASS", _(
        "please Select A Product Class"
    )
    BTL = "BTL", _("BTL")
    SECURED = "SECURED", _("Secured")
    RESIDENTIAL = "RESIDENTIAL", _("Residential")
    BRIDGING = "BRIDGING", _("Bridge")
    COMMERCIAL = "COMMERCIAL", _("Commercial")
    LET_TO_BUY = "LET_TO_BUY", _("Let To Buy")


class ArrangementFeeAddedToLoanChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class BookingFeeAddedToLoanChoices(models.TextChoices):
    SELECT = "--SELECT--", _("--Select--")
    NA = "NA", _("N/A")
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class DIPDecisionChoices(models.TextChoices):
    ACCEPTED = "ACCEPTED", _("Accepted")
    DECLINED = "DECLINED", _("Declined")
    REFERED = "REFERED", _("Refered")


class FeesChoices(models.TextChoices):
    FEES_IN = "FEES_IN", _("Fees In")
    FEES_OUT = "FEES_OUT", _("Fees Out")


class FeesInFeeTypeChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    BROKER_COMMITMENT_FEE = "BROKER_COMMITMENT_FEE", _("Broker Commit Fee")
    PROCURATION_FEE = "PROCURATION_FEE", _("Procuration Fee")
    MORTGAGE_OFFER_FEE = "MORTGAGE_OFFER_FEE", _("Mortgage Offer Fee")
    BROKER_FEE = "BROKER_FEE", _("Broker Fee")
    OTHER = "OTHER", _("Other")


class MethodChoices(models.TextChoices):
    CREDIT_DEBIT_CARD = "CREDIT_DEBIT_CARD", _("Credit Debit Card")
    BACS = "BACS", _("BACS")
    CHEQUE = "CHEQUE", _("Cheque")
    CASH = "CASH", _("Cash")
    ONLINE = "ONLINE", _("Online")
    OTHER = "OTHER", _("Other")


class FeesOutFeeTypeChoices(models.TextChoices):
    UNKNOWN = "UNKNOWN", _("Unknown")
    COMMISSION_PROC_FEE_SHARE = "COMMISSION_PROC_FEE_SHARE", _(
        "Commission Proc Fee Share"
    )


class IncomeTypeChoices(models.TextChoices):
    CURRENT_INCOME = "CurrentIncome", _("Current Income")
    POST_COMPLETION_INCOME = "PostCompletionIncome", _("Post Completion Income")


class DebtRepaymentTypeChoices(models.TextChoices):
    CURRENT_DEBT_REPAYMENTS = "CurrentDebtRepayments", _("Current Debt Repayments")
    POST_COMPLETION_DEBT_REPAYMENTS = "PostCompletionDebtRepayments", _(
        "Post Completion Debt Repayments"
    )


class PriorityDebtTypeChoices(models.TextChoices):
    CURRENT_PRIORITY_DEBT = "CurrentPriorityDebt", _("Current Priority Debt")
    POST_COMPLETION_PRIORITY_DEBT = "PostCompletionPriorityDebt", _(
        "Post Completion Priority Debt"
    )


class UnsecuredBorrowingTypeChoices(models.TextChoices):
    CURRENT_UNSECURED_BORROWING = "CurrentUnsecuredBorrowing", _(
        "Current Unsecured Borrowing"
    )
    POST_COMPLETION_UNSECURED_BORROWING = "PostCompletionUnsecuredBorrowing", _(
        "Post Completion Unsecured Borrowing"
    )


class LivingCostsTypeChoices(models.TextChoices):
    CURRENT_LIVING_COSTS = "CurrentLivingCosts", _("Current Living Costs")
    POST_COMPLETION_LIVING_COSTS = "PostCompletionLivingCosts", _(
        "Post Completion Living Costs"
    )


class InsuranceTypeChoices(models.TextChoices):
    CURRENT_INSURANCES = "CurrentInsurances", _("Current Insurances")
    POST_COMPLETION_INSURANCES = "PostCompletionInsurances", _(
        "Post Completion Insurances"
    )


class SubTotalsTypeChoices(models.TextChoices):
    CURRENT_SUB_TOTALS = "CurrentSubTotals", _("Current Sub Totals")
    POST_COMPLETION_SUB_TOTALS = "PostCompletionSubTotals", _(
        "Post Completion Sub Totals"
    )


class RegionChoices(models.TextChoices):
    PLEASE_SELECT_A_REGION = "PLEASE_SELECT_A_REGION", _("Please Select a Region")
    NORTH = "NORTH", _("North")
    NORTH_WEST = "NORTH_WEST", _("North West")
    YORKSHIRE_AND_HUMBERSIDE = "YORKSHIRE_AND_HUMBERSIDE", _("Yorkshire and Humberside")
    EAST_MIDLANDS = "EAST_MIDLANDS", _("East Midlands")
    WEST_MIDLANDS = "WEST_MIDLANDS", _("West Midlands")
    EAST_ANGLIA = "EAST_ANGLIA", _("East Anglia")
    LONDON = "LONDON", _("London")
    SOUTH_EAST = "SOUTH_EAST", _("South East (Not London)")
    SOUTH_WEST = "SOUTH_WEST", _("South West")
    WALES = "WALES", _("Wales")
    SCOTLAND = "SCOTLAND", _("Scotland")
    NORTHERN_IRELAND = "NORTHERN_IRELAND", _("Northern Ireland")


class CountryChoices(models.TextChoices):
    UNITED_KINGDOM = "UNITED_KINGDOM", _("United Kingdom")
    ENGLAND = "ENGLAND", _("England")
    SCOTLAND = "SCOTLAND", _("Scotland")
    WALES = "WALES", _("Wales")
    NORTHERN_IRELAND = "NORTHERN_IRELAND", _("Northern Ireland")


class PropertyTypeChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    HOUSE = "HOUSE", _("House")
    FLAT = "FLAT", _("Flat")
    MAISONETTE = "MAISONETTE", _("Maisonette")
    BUNGALOW = "BUNGALOW", _("Bungalow")
    WAREHOUSE = "WAREHOUSE", _("Warehouse")
    LAND = "LAND", _("Land")
    COMMERCIAL = "COMMERCIAL", _("Commercial")
    SEMI_COMMERCIAL = "SEMI_COMMERCIAL", _("Semi-Commercial")
    MULTI_UNIT_BLOCK = "MULTI_UNIT_BLOCK", _("Multi-Unit Block")
    HMO = "HMO", _("HMO")


class HouseTypeChoice(models.TextChoices):
    SELECT = "SELECT", _("Select")
    DETACHED = "DETACHED", _("Detached")
    SEMI_DETACHED = "SEMI_DETACHED", _("Semi-Detached")
    MID_TERRACED = "MID_TERRACED", _("Mid-Terraced")
    END_TERRACED = "END_TERRACED", _("End-Terraced")
    TOWN_HOUSE = "TOWN_HOUSE", _("Town House")


class FlatTypeChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    PURPOSE_BUILT = "PURPOSE_BUILT", _("Purpose Built")
    CONVERTED = "CONVERTED", _("Converted")
    STUDIO = "STUDIO", _("Studio")


class ConstructionOfWallsChoices(models.TextChoices):
    PLEASE_SELECT_A_CONSTRUCTION_TYPE = "PLEASE_SELECT_A_CONSTRUCTION_TYPE", _(
        "Please Select A Construction Type"
    )
    CONCRETE = "CONCRETE", _("Concrete")
    TIMBER_FRAMED = "TIMBER_FRAMED", _("Timber Framed")
    STEEL_FRAMED = "STEEL_FRAMED", _("Steel Framed")
    BRICK = "BRICK", _("Brick")
    MUNDIC_BLOCK = "MUNDIC_BLOCK", _("Mundic Block")
    PRC_REPAIR_WITH_CERTIFICATE = "PRC_REPAIR_WITH_CERTIFICATE", _(
        "PRC Repair with Certificate"
    )
    STONE = "STONE", _("Stone")
    COB = "COB", _("Cob")


class ConstructionOfRoofChoices(models.TextChoices):
    TILE_ANY_TYPE = "TILE_ANY_TYPE", _("Tile (Any Type)")
    CLAY_TILE = "CLAY_TILE", _("Clay Tile")
    SLATE_TILE = "SLATE_TILE", _("Slate Tile")
    CONCRETE_TILE = "CONCRETE_TILE", _("Concrete Tile")
    FLAT = "FLAT", _("Flat")
    THATCHED = "THATCHED", _("Thatched")
    METAL = "METAL", _("Metal")
    WOOD = "WOOD", _("Wood")
    PLASTIC_EG_EPDM_PVC_CPE = "PLASTIC_EG_EPDM_PVC_CPE", _(
        "Plastic (e.g. EPDM, PVC, CPE)"
    )
    BITUMEN = "BITUMEN", _("Bitumen")
    GREEN_ROOF = "GREEN_ROOF", _("Green Roof")
    SHINGLES = "SHINGLES", _("Shingles")
    OTHER = "OTHER", _("Other")


class ChargeTypeChoices(models.TextChoices):
    ONE = "ONE", _("One")
    TWO = "TWO", _("Two")
    THREE = "THREE", _("Three")
    FOUR = "FOUR", _("Four")
    FIVE = "FIVE", _("Five")
    SIX = "SIX", _("Six")
    SEVEN = "SEVEN", _("Seven")
    EIGHT = "EIGHT", _("Eight")
    NINE = "NINE", _("Nine")
    TEN = "TEN", _("Ten")


class EpcRatingChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    A = "A", _("A")
    B = "B", _("B")
    C = "C", _("C")
    D = "D", _("D")
    E = "E", _("E")
    F = "F", _("F")
    G = "G", _("G")


class TenureChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    FREEHOLD = "FREEHOLD", _("Freehold")
    LEASEHOLD = "LEASEHOLD", _("Leasehold")
    COMMONHOLD = "COMMONHOLD", _("Commonhold")
    FEUDAL = "FEUDAL", _("Feudal")


class ListedStatusOfTheBuildingChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    GRADE_I = "GRADE_I", _("Grade I")
    GRADE_II_STAR = "GRADE_II*", _("Grade II*")
    GRADE_II = "GRADE_II", _("Grade II")
    GRADE_A = "GRADE_A", _("Grade A")
    GRADE_B = "GRADE_B", _("Grade B")
    GRADE_C = "GRADE_C", _("Grade C")


class NewBuildWarrantyProviderChoices(models.TextChoices):
    SELECT_WARRANTY_PROVIDER = "SELECT_WARRANTY_PROVIDER", _("Select Warranty Provider")
    NHBC = "NHBC", _("NHBC")
    LABC = "LABC", _("LABC")
    PREMIER_GUARANTEE = "PREMIER_GUARANTEE", _("Premier Guarantee")
    CHECKMATE = "CHECKMATE", _("Checkmate")
    BUILDSAFE = "BUILDSAFE", _("Buildsafe")
    BUILD_ZONE = "BUILD_ZONE", _("Build Zone")
    ICW = "ICW", _("ICW")
    PRO_TEK = "PRO_TEK", _("Pro Tek")
    GLOBAL = "GLOBAL", _("Global")
    OTHER = "OTHER", _("Other")


class ValuationTypeChoices(models.TextChoices):
    STANDARD_VAL = "standard_val", _("Standard Val")
    HOMEBUYERS = "homebuyers", _("Homebuyers")
    FULL_STANDARD_BUILDING_SURVEY = "full_standard_building_survey", _(
        "Full Standard Building Survey"
    )
    AVM = "avm", _("AVM")
    DRIVE_BY = "drive_by", _("Drive By")


class SelectApplicantListChoices(models.TextChoices):
    SELECT = "SELECT", _("Select")
    DEMO_X = "demo_x", _("Demo X")


class RelationshipChoices(models.TextChoices):
    PARTNER = "partner", _("Partner")
    SPOUSE = "spouse", _("Spouse")
    SIBLING = "sibling", _("Sibling")
    PARENT = "parent", _("Parent")
    CARER = "carer", _("Carer")
    FAMILY = "family", _("Family")
    OTHER_FAMILY = "other_family", _("Other Family")
    OTHER = "other", _("Other")
    CHILD = "child", _("Child")
    CIVIL_PARTNER = "civil_partner", _("Civil Partner")
    SON = "son", _("Son")
    DAUGHTER = "daughter", _("Daughter")
    GRANDPARENT = "grandparent", _("Grandparent")
    BROTHER = "brother", _("Brother")
    SISTER = "sister", _("Sister")
    UNCLE_AUNT = "uncle_aunt", _("Uncle/Aunt")
    FOSTER_ADOPTIVE_PARENTS = "foster_adoptive_parents", _("Foster/Adoptive Parents")
    LEGAL_GUARDIAN = "legal_guardian", _("Legal Guardian")
