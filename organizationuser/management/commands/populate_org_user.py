from django.core.management.base import BaseCommand
from authentication.models import User  # Import your custom User model
from common.enums import RoleChoices
from organization.models import Organization  # Replace with your app name


class Command(BaseCommand):
    help = "Populate organization with advisor users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--org',
            type=str,
            help="Name of the organization to populate users for"
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help="Number of advisor users to create"
        )

    def handle(self, *args, **kwargs):
        org_name = kwargs['org']
        user_count = kwargs['count']

        if not org_name:
            self.stderr.write(self.style.ERROR("Organization name is required. Use --org."))
            return

        try:
            organization = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Organization '{org_name}' does not exist."))
            return

        for i in range(1, user_count + 1):
            email = f'advisor_{org_name.lower()}_{i}@example.com'

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f"User {email} already exists. Skipping."))
                continue

            # Create the user
            user = User.objects.create_user(
                email=email,
                username=email.split('@')[0],
                password="defaultpassword123",  # Replace with a secure mechanism
                role=RoleChoices.ADVISOR,  # Assuming your RoleChoices contains ADVISOR
            )
            user.save()

            # Output success message
            self.stdout.write(self.style.SUCCESS(
                f"Created user: {email} and assigned ADVISOR role in {org_name}."
            ))
