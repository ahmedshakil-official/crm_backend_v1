from django.db import models
from django.utils.translation import gettext_lazy as _


class ApplicationTypeChoices(models.TextChoices):
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
