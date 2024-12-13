from django.core.management.base import BaseCommand
from organization.models import Organization

class Command(BaseCommand):
    help = "Create 5 organizations."

    def handle(self, *args, **kwargs):
        organizations = [
            {
                "name": "QOP",
                "email": "qop@example.com",
                "primary_mobile": "+1234567890"
            },
            {
                "name": "Health OS",
                "email": "healthos@example.com",
                "primary_mobile": "+1234567891"
            },
            {
                "name": "Repliq LTD",
                "email": "repliqltd@example.com",
                "primary_mobile": "+1234567892"
            },
            {
                "name": "Therap BD",
                "email": "therapbd@example.com",
                "primary_mobile": "+1234567893"
            },
            {
                "name": "Optimizly",
                "email": "optimizly@example.com",
                "primary_mobile": "+1234567894"
            },
        ]

        for org_data in organizations:
            org, created = Organization.objects.get_or_create(
                name=org_data["name"],
                defaults={
                    "email": org_data["email"],
                    "primary_mobile": org_data["primary_mobile"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Organization created: {org_data['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Organization already exists: {org_data['name']}"))
