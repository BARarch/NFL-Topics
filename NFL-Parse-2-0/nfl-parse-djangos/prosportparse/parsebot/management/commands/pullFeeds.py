from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article
#from parsebot.parsebot_classes.parseConfig import ParseConfig
#import parsebot.parsebot_classes.modelGS as mgs

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets

class Command(BaseCommand):
	help = 'Pulls feeds from in the group assigned to the app'

	def add_arguments(self, parser):
		parser.add_argument('arg', nargs='+', type=str)

	def handle(self, *args, **options):
		## Opening Message

		SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    	CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
    	APPLICATION_NAME = 'NFL-Parse'

    	flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES)
    	flow.user_agent = APPLICATION_NAME

		print('hello world {} says hi'.format(options['arg'][0]))
		print('Session Started')

		credentials = creds
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http=http,
								  discoveryServiceUrl=discoveryUrl)

		spreadsheet_id = '1lJa1YVucaoDI0DW0VdyaJza8uAmvjGPdL-krRLiaMuc'
		value_input_option = 'RAW'
		rangeName = 'RUNS!A' + '3'
		values = [['Hello From Django']]
		body = {
		  'values': values
		}
	
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
														valueInputOption=value_input_option, body=body).execute()

		print('finished')


		## Step 1: Establish Config Object

		## Step 2: Read Sheet

		## Step 3: Get Objects from Model

		## Step 4: Pull Articles from Feeds in Group

		## Last Step: Finnish up with Some Output