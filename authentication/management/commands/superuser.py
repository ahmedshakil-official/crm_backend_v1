from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser without password validation"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email="m@m.com").exists():
            User.objects.create_superuser(
                email="a@admin.com",
                password="admin",  # Choose a dev-only password
                first_name="Mahbub",
                last_name="Rahman",
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully!"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
