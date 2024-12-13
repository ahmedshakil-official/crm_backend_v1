from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from organization.models import Organization, OrganizationUser
from common.enums import RoleChoices, UserTypeChoices
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Create 20 Advisors, 20 Leads, 20 Introducers, and 20 Clients for each organization."

    def handle(self, *args, **kwargs):
        # Fetch all organizations
        organizations = Organization.objects.all()

        if not organizations.exists():
            self.stdout.write(self.style.ERROR("No organizations found. Please create organizations first."))
            return

        # Function to generate random phone numbers
        def random_phone():
            return f"+1{random.randint(1000000000, 9999999999)}"

        # Function to generate random email
        def random_email(role, org_name, index):
            return f"{role.lower()}_{org_name.lower()}_{index}@example.com"

        for org in organizations:
            self.stdout.write(self.style.SUCCESS(f"Processing organization: {org.name}"))

            for role, user_type in [
                (RoleChoices.ADVISOR, UserTypeChoices.ADVISOR),
                (RoleChoices.LEAD, UserTypeChoices.LEAD),
                (RoleChoices.INTRODUCER, UserTypeChoices.INTRODUCER),
                (RoleChoices.CLIENT, UserTypeChoices.CLIENT),
            ]:
                for i in range(1, 21):
                    # Create user
                    first_name = f"{role.capitalize()}_{i}"
                    last_name = f"User_{i}"
                    email = random_email(role, org.name, i)
                    phone = random_phone()

                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={
                            "first_name": first_name,
                            "last_name": last_name,
                            "password": "Admin.1234",
                            "phone": phone,
                            "user_type": user_type,
                            "is_active": True,
                        },
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created user: {email}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"User already exists: {email}"))

                    # Create organization user
                    org_user, org_user_created = OrganizationUser.objects.get_or_create(
                        user=user,
                        organization=org,
                        defaults={"role": role},
                    )

                    if org_user_created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Assigned {role} role to {email} in {org.name}")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"User {email} is already assigned as {role} in {org.name}"
                            )
                        )

        self.stdout.write(self.style.SUCCESS("Completed creating users for all organizations."))
