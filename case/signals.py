from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save, sender="case.Case")  # Change sender to string
def create_loan_details(sender, instance, created, **kwargs):
    if created:
        LoanDetails = apps.get_model("case", "LoanDetails")  # Move this inside function
        LoanDetails.objects.create(case=instance)


@receiver(post_save, sender="case.Case")  # Using string reference for dynamic model loading
def create_applicant_details(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model("case", "ApplicantDetails")  # Dynamically get ApplicantDetails model

        # Ensure only one ApplicantDetails instance is created
        ApplicantDetails.objects.create(
            case=instance,
            applicant=instance.lead,  # Always assign the lead as the applicant
        )


@receiver(post_save, sender="case.JointUser")  # Using string reference for dynamic loading
def create_applicant_details_for_joint_user(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model("case", "ApplicantDetails")  # Get ApplicantDetails model dynamically

        # Create ApplicantDetails for the joint user
        ApplicantDetails.objects.create(
            case=instance.case,
            applicant=instance.joint_user,  # Assigning the joint user as the applicant
        )