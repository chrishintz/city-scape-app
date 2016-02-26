from django.core.management.base import BaseCommand, CommandError
from cityscape.weather import Weather

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("test")
