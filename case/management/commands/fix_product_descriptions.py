from django.core.management.base import BaseCommand
from case.models import Product


class Command(BaseCommand):
    help = "Fix NULL product_description values"

    def handle(self, *args, **options):
        # Update all NULL product_description values
        updated = Product.objects.filter(product_description__isnull=True).update(
            product_description="No description provided"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated} Product records with NULL product_description"
            )
        )
