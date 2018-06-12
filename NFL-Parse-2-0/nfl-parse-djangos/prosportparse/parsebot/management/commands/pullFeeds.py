from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article
from parsebot.parsebot_classes.parseConfig import ParseConfig


class Command(BaseCommand):
    help = 'Pulls feeds from in the group assigned to the app'

    def add_arguments(self, parser):
        parser.add_argument('arg', nargs='+', type=str)

    def handle(self, *args, **options):
        ## Opening Message
        print('hello world {} says hi'.format(options['arg'][0]))
        print('Session Started')

        session = ParseConfig('hello', 'world')


        ## Step 1: Establish Config Object

        ## Step 2: Read Sheet

        ## Step 3: Get Objects from Model

        ## Step 4: Pull Articles from Feeds in Group

        ## Last Step: Finnish up with Some Output