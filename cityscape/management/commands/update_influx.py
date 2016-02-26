from django.core.management.base import BaseCommand, CommandError
from cityscape.influx import Influx

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Refreshing Influx data...")
        refreshed_count = Influx.update_data()
        print(refreshed_count)
