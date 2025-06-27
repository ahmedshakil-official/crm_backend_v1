from django.core.management.base import BaseCommand
from case.models import BudgetPlanner, DebtRepayments
from case.enums import DebtRepaymentTypeChoices


class Command(BaseCommand):
    help = "Fix NULL post_debt_repayments references in BudgetPlanner"

    def handle(self, *args, **options):
        # Find BudgetPlanners with NULL post_debt_repayments
        budget_planners_with_null = BudgetPlanner.objects.filter(
            post_debt_repayments__isnull=True
        )

        count = 0
        for budget_planner in budget_planners_with_null:
            # Create a new DebtRepayments record
            debt_repayment = DebtRepayments.objects.create(
                repayment_type=DebtRepaymentTypeChoices.POST_COMPLETION_DEBT_REPAYMENTS,
                total_debt_repayment=0.00,
            )

            # Link it to the budget planner
            budget_planner.post_debt_repayments = debt_repayment
            budget_planner.save()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created DebtRepayments records for {count} BudgetPlanner instances"
            )
        )
