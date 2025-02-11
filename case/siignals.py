from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Case, LoanDetails

@receiver(post_save, sender=Case)
def create_loan_details(sender, instance, created, **kwargs):
    if created:
        LoanDetails.objects.create(case=instance)