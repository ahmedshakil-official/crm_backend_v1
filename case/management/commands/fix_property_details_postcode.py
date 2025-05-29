from django.core.management.base import BaseCommand
from case.models import PropertyDetails


class Command(BaseCommand):
    help = 'Fix NULL postcode values in PropertyDetails'

    def handle(self, *args, **options):
        # Update all NULL postcode values with a default value
        updated = PropertyDetails.objects.filter(
            postcode__isnull=True
        ).update(
            postcode='TBD'  # To Be Determined - you can use any appropriate default
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated} PropertyDetails records with NULL postcode'
            )
        )