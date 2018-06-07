from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article

class Command(BaseCommand):
    help = 'Configures App for your group of feeds'

    def add_arguments(self, parser):
        parser.add_argument('arg', nargs='+', type=str)

    def handle(self, *args, **options):
    	pass