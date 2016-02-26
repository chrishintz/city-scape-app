from django.core.management.base import BaseCommand, CommandError
from cityscape.pets import Pets

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Refreshing Pet data...")
        Pets.update_data()
        
