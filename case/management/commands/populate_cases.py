from django.core.management.base import BaseCommand
from django.db import transaction
from case.models import Case
from organization.models import Organization, OrganizationUser
from common.enums import ProductCategoryChoices, ApplicantTypeChoices, CaseStatusChoices, CaseStageChoices
import random
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Create 200 cases for 5 organizations, each created by their ADVISOR and assigned to the LEAD"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Fetch 5 organizations
        organizations = Organization.objects.all()[:5]

        cases_to_create = []

        for organization in organizations:
            # Fetch the LEAD user for the organization (role="LEAD")
            lead_user = OrganizationUser.objects.filter(
                organization=organization, role="LEAD"
            ).select_related('user').first()

            # Fetch the ADVISOR users for the organization (role="ADVISOR")
            advisors = OrganizationUser.objects.filter(
                organization=organization, role="ADVISOR"
            ).select_related('user')

            if not lead_user:
                self.stdout.write(self.style.ERROR(f"No lead found for organization {organization.name}"))
                continue

            if not advisors:
                self.stdout.write(self.style.ERROR(f"No advisors found for organization {organization.name}"))
                continue

            # Create 40 cases for each organization (to make a total of 200)
            for _ in range(40):
                advisor = random.choice(advisors).user  # Randomly select an advisor for this case
                lead = lead_user.user  # The lead user for this case

                # Randomly choose values for the case fields
                case_category = random.choice(ProductCategoryChoices.choices)[0]
                applicant_type = random.choice(ApplicantTypeChoices.choices)[0]
                case_status = random.choice(CaseStatusChoices.choices)[0]
                case_stage = random.choice(CaseStageChoices.choices)[0]

                # Prepare the case instance
                case = Case(
                    organization=organization,
                    lead=lead,  # Assign the case to the organization's lead
                    created_by=advisor,  # The advisor is the creator of the case
                    case_category=case_category,
                    applicant_type=applicant_type,
                    case_status=case_status,
                    case_stage=case_stage,
                    created_at=now(),
                    updated_at=now()
                )

                cases_to_create.append(case)

        # Bulk create all the cases at once
        Case.objects.bulk_create(cases_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(cases_to_create)} cases"))
