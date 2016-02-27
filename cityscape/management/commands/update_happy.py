from django.core.management.base import BaseCommand, CommandError
from cityscape.happy import Happy

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Refreshing Happy data...")
        Happy.update_data()
