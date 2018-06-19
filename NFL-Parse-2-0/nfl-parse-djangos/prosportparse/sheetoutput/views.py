import os
#import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.conf import settings

from sheetoutput.models import CredetialsModel

from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.client import flow_from_clientsecrets


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
APPLICATION_NAME = 'ParseBot-SheetOutput'

flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES, redirect_uri='http://localhost:8080/oath2callback')
print('got flow')

# Create your views here.
@login_required
def authorize(request):
	print(request.user)
	print(type(request.user))

	storage = DjangoORMStorage(	CredetialsModel, 
								'user_id', 
								request.user, 
								'credential')
	
	print('got storage object...')
	cred = storage.get()

	if cred is None or cred.invalid == True:
		flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
														request.user)
		print('we have not valid credential stored')
		print('we are using flow to generate token')
		print(flow.params)
		authorize_url = flow.step1_get_authorize_url()
		print('going to authorize... \nauthorize_url: {}'.format(str(authorize_url)))
		## If the flow is bad we might have to go to Google developers console
		## and get a new server to server secret for this django.
		return HttpResponseRedirect(authorize_url)
	else:
		http = httplib2.Http()
		http = cred.authorize(http)
		print('Credential Authorized')
		return render(request, 'sheetoutput/welcome.html', {})



@login_required
def auth_return(request):
	print(request.user)
	print(type(request.user))
	if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'].encode('UTF-8'), request.user):
		return HttpResponseBadRequest()
	
	cred = flow.step2_exchange(request.GET)
	storage = DjangoORMStorage(CredetialsModel, 'user_id', request.user, 'credential')
	storage.put(cred)
	print('credential done: check admin')
	return HttpResponseRedirect("/auth")
	