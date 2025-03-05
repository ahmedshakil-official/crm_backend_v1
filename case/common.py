from django.db import models

from authentication.models import User
from case.enums import CommitmentTypeChoices, PlanChoices
from case.models import Adverse
from common.models import CreatedAtUpdatedAtBaseModel


class RegisterLoan(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="register"
    )

    amount = models.DecimalField(decimal_places=2, max_digits=20)
    loan_company_name = models.CharField(max_length=200, null=True, blank=True)
    date_registered = models.DateField(null=True, blank=True)
    has_satisfied = models.BooleanField(default=False)
    date_satisfied = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class PaymentCommitment(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="payment_commitment"
    )

    commitment_type = models.CharField(
        max_length=50,
        choices=CommitmentTypeChoices.choices,
        default=CommitmentTypeChoices.UNKNOWN,
    )
    loan_company_name = models.CharField(max_length=200, null=True, blank=True)
    date_cleared = models.DateField(null=True, blank=True)
    missed_payments_in_the_last_three_months = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    missed_payments_in_the_last_twelve_months = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    missed_payments_in_the_last_twenty_four_months = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    missed_payments_in_the_last_thirty_six_months = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    missed_payments_in_the_last_sixty_months = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class PropertyRepossessed(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="property_repossessed"
    )

    lender = models.CharField(max_length=100, null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    date_of_satisfaction = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class Bankrupt(CreatedAtUpdatedAtBaseModel):
    date_discharged = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class IndividualVoluntary(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="individual_voluntary"
    )

    date_registered = models.DateField(null=True, blank=True)
    outstanding_balance = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    satisfied = models.BooleanField(default=False)
    date_satisfied = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class DebtManagementPlan(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="debt_management_plan"
    )

    plan = models.CharField(
        max_length=20, choices=PlanChoices.choices, default=PlanChoices.DIRECT
    )
    loan_company_name = models.CharField(max_length=200, null=True, blank=True)
    date_registered = models.DateField(null=True, blank=True)
    outstanding_balance = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    satisfied = models.BooleanField(default=False)
    date_satisfied = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class PayDayLoan(CreatedAtUpdatedAtBaseModel):
    adverse = models.ForeignKey(
        Adverse, on_delete=models.CASCADE, related_name="payday_loan"
    )

    loan_amount = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    loan_date = models.DateField(null=True, blank=True)
    has_the_pay_day_loan_been_repaid = models.BooleanField(default=False)
    date_repaid = models.DateField(null=True, blank=True)
    lender_name = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        ordering = ["-created_at", "-updated_at"]