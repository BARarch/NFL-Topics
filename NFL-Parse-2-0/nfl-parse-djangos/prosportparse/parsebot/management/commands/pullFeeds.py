from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article

class Command(BaseCommand):
    help = 'Pulls feeds from in the group assigned to the app'

    def add_arguments(self, parser):
        parser.add_argument('arg', nargs='+', type=str)

    def handle(self, *args, **options):
        print('hello world {} says hi'.format(options['arg'][0]))

        options