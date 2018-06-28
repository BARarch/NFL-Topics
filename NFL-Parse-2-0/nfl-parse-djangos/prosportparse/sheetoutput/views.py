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
from oauth2client.contrib.django_util.storage import DjangoORMStorage


import google.oauth2.credentials
import google.auth.transport.requests
import requests

from google_auth_oauthlib.flow import Flow


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
APPLICATION_NAME = 'ParseBot-SheetOutput'
REDIRECT_URI = 'http://localhost:8080/oath2callback'

SESSION = {}  ## for credentials and state

STORAGE = DjangoORMStorage(    CredetialsModel, 
								'user_id', 
								1, 
								'credential')




@login_required
def authorize(request):
	# Flow
	flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE,
										 scopes=[SCOPES])
	flow.redirect_uri = REDIRECT_URI
	authorization_url, state = flow.authorization_url(access_type='offline',
													  prompt='consent',
													  include_granted_scopes='true')
	SESSION['state'] = state
	print(list(request.GET.items()))
	return HttpResponseRedirect(authorization_url)

@login_required
def auth_return(request):
	state = SESSION['state']
	flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE,
										 scopes=[SCOPES],
										 state=state)
	flow.redirect_uri = REDIRECT_URI
	
	#print(list(request.GET.items()))

	responseWithCode = request.build_absolute_uri()
	flow.fetch_token(authorization_response=responseWithCode)
	credentials = flow.credentials
	SESSION['credentials'] = credentials_to_dict(credentials)
	
	print(SESSION['credentials'])
	STORAGE.put(credentials)
	return

@login_required
def refresh_token(request):
	
	cred = force_refresh()

	return render(request, 'sheetoutput/message.html', {'outcome': 'the token has been refeshed and is valid until {}'.format(str(credentials_to_dict(cred)['expiry']))})

@login_required
def check_token(request):
	print('Checking for the owners token...')
	cred = STORAGE.get()

	print(dict_to_string(credentials_to_dict(cred)))

	if cred.expired == True:
		return HttpResponseRedirect('/refresh')
	else:
		return render(request, 'sheetoutput/message.html', {'outcome': 'the token we have is valid until {}'.format(str(credentials_to_dict(cred)['expiry']))})

@login_required
def touch(request):
	cred = STORAGE.get()

	if cred is None:
		print('No Credentials for sheetoutput')
		return render(request, 'sheetoutput/message.html', {'outcome': 'No Credentials, please authenticate parsebot sheetoutput!'})
	if cred.expired == True:
		cred = force_refresh()

	http = cred.authorize(httplib2.Http())
	print('TOUCH complete')
	return render(request, 'sheetoutput/message.html', {'outcome': 'The call to the google sheet has completed!'})

def get_storage_for_owner():
	return DjangoORMStorage(    CredetialsModel, 
								'user_id', 
								1, 
								'credential')

def credentials_to_dict(credentials):
	return {'token': credentials.token,
			'refresh_token': credentials.refresh_token,
			'expiry': credentials.expiry,
			'expired': credentials.expired,
			'token_uri': credentials.token_uri,
			'client_id': credentials.client_id,
			'client_secret': credentials.client_secret,
			'scopes': credentials.scopes}

def dict_to_string(dictt):
	return 'Creds {\n' + '\n'.join(["\t'{}': {},".format(str(item), str(dictt[item])) for item in dictt]) + '\n}'

def force_refresh():
	## Force Refresh for token with Google transport HTTP object
	cred = STORAGE.get()
	print('refreshing token...')
	print(dict_to_string(credentials_to_dict(cred)))

	requestt = google.auth.transport.requests.Request()
	cred.refresh(requestt)

	STORAGE.put(cred)

	return cred


	