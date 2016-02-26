from django.core.management.base import BaseCommand, CommandError
from cityscape.traffic import Traffic

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Refreshing Traffic data...")
        refreshed_count = Traffic.update_data()
        print(refreshed_count)
