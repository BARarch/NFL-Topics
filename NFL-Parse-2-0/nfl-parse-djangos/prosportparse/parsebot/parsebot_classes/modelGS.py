from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = '_client_secret.json'
    APPLICATION_NAME = 'NFL-Parse'

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.NFL-Parse.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
            
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def modelInit():
    print('Initializing Google Model')
    try:
        import argparse

        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        print('did flags set?')
    except ImportError:
        print('We got import trouble')
        flags = None

    except Exception as e:
        print(str(e))
    print('Finnished')


    
    return get_credentials

if __name__ == "__main__":
    rais = modelInit()
    creds = rais()
    print('do you have new creds')

    credentials = creds
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1lJa1YVucaoDI0DW0VdyaJza8uAmvjGPdL-krRLiaMuc'
    value_input_option = 'RAW'
    rangeName = 'RUNS!A' + '2'
    values = [['Hello World']]
    body = {
          'values': values
    }
    
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                        valueInputOption=value_input_option, body=body).execute()