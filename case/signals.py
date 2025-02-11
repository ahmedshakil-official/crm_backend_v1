from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='case.Case')  # Change sender to string
def create_loan_details(sender, instance, created, **kwargs):
    if created:
        LoanDetails = apps.get_model('case', 'LoanDetails')  # Move this inside function
        LoanDetails.objects.create(case=instance)
