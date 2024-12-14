from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from authentication.models import User
from organization.models import (
    Organization,
    OrganizationUser,
)  # Adjust app names accordingly
from common.enums import RoleChoices, GenderChoices, UserTypeChoices


class Command(BaseCommand):
    help = "Populate organizations with users of different roles"

    def handle(self, *args, **kwargs):
        # Fetch all organizations
        organizations = Organization.objects.all()

        if not organizations.exists():
            self.stderr.write("No organizations found.")
            return

        # Iterate through each organization
        for _ in range(200):
            for org in organizations:
                self.stdout.write(f"Processing organization: {org.name}")

                # Create a LEAD user
                self.create_user_for_organization(
                    org, UserTypeChoices.LEAD, RoleChoices.LEAD
                )

                # Create a CLIENT user
                self.create_user_for_organization(
                    org, UserTypeChoices.CLIENT, RoleChoices.CLIENT
                )

                # Create an ADVISOR user
                self.create_user_for_organization(
                    org, UserTypeChoices.ADVISOR, RoleChoices.ADVISOR
                )

                # Create an INTRODUCER user
                self.create_user_for_organization(
                    org, UserTypeChoices.INTRODUCER, RoleChoices.INTRODUCER
                )

    def create_user_for_organization(self, org, user_type, role):
        # Generate unique user details
        email = f"{user_type.lower()}_{org.slug}_{get_random_string(5)}@example.com"
        phone = f"+1234567{get_random_string(4, '0123456789')}"
        first_name = f"{user_type.title()}"
        last_name = "User"
        password = "securepassword"

        # Create the user
        user = User.objects.create_user(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            password=password,
        )

        # Assign to OrganizationUser
        OrganizationUser.objects.create(
            user=user,
            organization=org,
            role=role,
            gender=GenderChoices.MALE,  # Replace with logic if dynamic gender is needed
        )

        self.stdout.write(
            f"Created {user_type} user: {email} and assigned {role} role in {org.name}"
        )
