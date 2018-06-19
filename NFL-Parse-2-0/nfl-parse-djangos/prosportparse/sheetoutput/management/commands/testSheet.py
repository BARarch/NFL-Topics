from django.conf import settings

from django.core.management.base import BaseCommand, CommandError
from parsebot.models import Article
from sheetoutput.models import CredetialsModel

from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets


class Command(BaseCommand):
	help = 'Pulls feeds from in the group assigned to the app'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		print('from Test Sheet Management Command')

		SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
		CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
		APPLICATION_NAME = 'ParseBot-SheetOutput'

		flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES, redirect_uri='http://localhost:8080/oath2callback')
		print('got flow')

		storage = DjangoORMStorage(	CredetialsModel, 
									'user_id', 
									0, 
									'credential')
		print('got storage object')

		cred = storage.get()
		print(cred)
		print(storage)

		if cred is None or credential.invalid == True:
			flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
															0)
			print('we have not valid credential stored')
			print('we are using flow to generate token')
			print(flow.params)
			authorize_url = flow.step1_get_authorize_url()
			print('authorize_url: {}'.format(str(authorize_url)))
			## If the flow is bad we might have to go to Google developers console
			## and get a new server to server secret for this django.
		else:
			print('Now to authorize credential with HTTPlib2')