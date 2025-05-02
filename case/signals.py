from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save, sender="case.Case")  # Change sender to string
def create_loan_details(sender, instance, created, **kwargs):
    if created:
        LoanDetails = apps.get_model("case", "LoanDetails")  # Move this inside function
        LoanDetails.objects.create(case=instance)


@receiver(
    post_save, sender="case.Case"
)  # Using string reference for dynamic model loading
def create_applicant_details(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model(
            "case", "ApplicantDetails"
        )  # Dynamically get ApplicantDetails model

        # Ensure only one ApplicantDetails instance is created
        ApplicantDetails.objects.create(
            case=instance,
            applicant=instance.lead,  # Always assign the lead as the applicant
        )


@receiver(
    post_save, sender="case.JointUser"
)  # Using string reference for dynamic loading
def create_applicant_details_for_joint_user(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model(
            "case", "ApplicantDetails"
        )  # Get ApplicantDetails model dynamically

        # Create ApplicantDetails for the joint user
        ApplicantDetails.objects.create(
            case=instance.case,
            applicant=instance.joint_user,  # Assigning the joint user as the applicant
        )


@receiver(post_save, sender="case.Case")
def create_employment_details_for_lead(sender, instance, created, **kwargs):
    """
    When a new Case is created, automatically create an EmploymentDetails record
    for the 'lead' user.
    """
    if created:
        EmploymentDetails = apps.get_model("case", "EmploymentDetails")
        EmploymentDetails.objects.create(
            case=instance,
            user=instance.lead,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.JointUser")
def create_employment_details_for_joint_user(sender, instance, created, **kwargs):
    """
    When a new JointUser is created for a case, automatically create an EmploymentDetails
    record for that joint user.
    """
    if created:
        EmploymentDetails = apps.get_model("case", "EmploymentDetails")
        EmploymentDetails.objects.create(
            case=instance.case,
            user=instance.joint_user,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.Case")
def create_adverse_for_lead(sender, instance, created, **kwargs):
    """
    When a new Case is created, automatically create an EmploymentDetails record
    for the 'lead' user.
    """
    if created:
        Adverse = apps.get_model("case", "Adverse")
        Adverse.objects.create(
            case=instance,
            user=instance.lead,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.JointUser")
def create_adverse_for_joint_user(sender, instance, created, **kwargs):
    """
    When a new JointUser is created for a case, automatically create an EmploymentDetails
    record for that joint user.
    """
    if created:
        Adverse = apps.get_model("case", "Adverse")
        Adverse.objects.create(
            case=instance.case,
            user=instance.joint_user,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.Case")
def create_existing_protection_for_lead(sender, instance, created, **kwargs):
    if created:
        ExistingProtection = apps.get_model("case", "ExistingProtection")
        ExistingProtection.objects.create(
            case=instance,
            user=instance.lead,
        )


@receiver(post_save, sender="case.JointUser")
def create_existing_protection_for_joint_user(sender, instance, created, **kwargs):
    if created:
        ExistingProtection = apps.get_model("case", "ExistingProtection")
        ExistingProtection.objects.create(
            case=instance.case,
            user=instance.joint_user,
        )


@receiver(post_save, sender="case.Case")
def create_property_details(sender, instance, created, **kwargs):

    if created:
        PropertyDetails = apps.get_model("case", "PropertyDetails")
        PropertyDetails.objects.create(case=instance)


@receiver(post_save, sender="case.Case")
def create_budget_planner(sender, instance, created, **kwargs):
    if created:
        BudgetPlanner = apps.get_model("case", "BudgetPlanner")
        BudgetPlanner.objects.create(case=instance)


@receiver(post_save, sender="case.Case")
def create_product(sender, instance, created, **kwargs):
    if created:
        Product = apps.get_model("case", "Product")
        Product.objects.create(case=instance)



@receiver(post_save, sender="case.Case")
def create_mortgage_needs(sender, instance, created, **kwargs):
    if created:
        MortgageNeeds = apps.get_model("case", "MortgageNeeds")
        MortgageNeeds.objects.create(case=instance)


@receiver(post_save, sender="case.Case")
def create_mortgage_features(sender, instance, created, **kwargs):
    if created:
        MortgageNeeds = apps.get_model("case", "MortgageFeatures")
        MortgageNeeds.objects.create(case=instance, applicant=instance.lead)



@receiver(post_save, sender="case.JointUser")
def create_mortgage_features_for_joint_user(sender, instance, created, **kwargs):
    if created:
        MortgageNeeds = apps.get_model("case", "MortgageFeatures")
        MortgageNeeds.objects.create(case=instance.case, applicant=instance.joint_user)

@receiver(post_save, sender="case.Case")
def create_suitability(sender, instance, created, **kwargs):
    if created:
        # Load necessary models
        Suitability = apps.get_model("case", "Suitability")

        # Mapping: field name in Suitability -> Model class name
        model_mapping = {
            'circumstances_objectives': 'CircumstancesObjectives',
            'budget_affordability': 'BudgetAffordability',
            'new_mortgage_details': 'NewMortgageDetails',
            'recommending_repayment_method': 'RecommendingRepaymentMethod',
            'recommending_mortgage_type': 'RecommendingMortgageType',
            'recommending_term': 'RecommendingTerm',
            'recommending_mortgage_lender': 'RecommendingMortgageLender',
            'recommending_mortgage_amount': 'RecommendingMortgageAmount',
            'costs_fees': 'CostsFees',
            'disadvantage_risks': 'DisadvantageRisks',
            'cost_advice': 'CostAdvice',
            'protection': 'Protection',
            'buildings_insurance': 'BuildingsInsurance',
            'wills': 'Wills',
        }

        # Step 1: Create empty Suitability linked to Case
        suitability = Suitability.objects.create(case=instance)

        # Step 2: Loop through all sub-models
        for field_name, model_name in model_mapping.items():
            model_class = apps.get_model("case", model_name)
            sub_instance = model_class.objects.create()

            setattr(suitability, field_name, sub_instance)

        # Step 3: Save Suitability after assigning all fields
        suitability.save()



@receiver(post_save, sender="case.Case")
def create_compliance(sender, instance, created, **kwargs):
    if created:
        Compliance = apps.get_model("case", "Compliance")
        Compliance.objects.create(case=instance)


@receiver(post_save, sender="case.Case")
def create_mortgage_needs(sender, instance, created, **kwargs):
    if created:
        MortgageNeeds = apps.get_model("case", "MortgageNeeds")
        MortgageNeeds.objects.create(case=instance)