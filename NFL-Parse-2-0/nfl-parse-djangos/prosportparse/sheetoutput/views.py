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


import google.oauth2.credentials
import google_auth_oauthlib.flow


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
APPLICATION_NAME = 'ParseBot-SheetOutput'
SESSION = {}  ## for credentials and state

@login_required
def authorize(request):
	return

@login_required
def auth_return(request):
	return

@login_required
def refresh_token(request):
	return

@login_required
def check_token(request):
	return




	