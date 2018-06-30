from sheetoutput.sheetoutput_classes.creds import Cred
from sheetoutput.models import SheetModel

import os
import httplib2

from googleapiclient.discovery import build

class SheetOutput:
	Sheet = SheetModel.objects.last()
	GroupName = Sheet.name
	SheetUrl = Sheet.sheetID
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	cred = Cred()

	def __init__(self):
		self.currentRow = 0
		pass

	def say_hello(self):
		
		service = build('sheets', 
						'v4', 
						credentials=SheetOutput.cred.get_cred(),
						discoveryServiceUrl=SheetOutput.discoveryUrl)

		spreadsheet_id = SheetOutput.SheetUrl
		value_input_option = 'RAW'
		rangeName = 'DjangoTest!D' + '1'
		values = [['hello world from django sheetoutput class']]
		body = {
			  'values': values
		}
		
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
														valueInputOption=value_input_option, body=body).execute()



class FeedList(SheetOutput):
	pass

class ExceptionList(SheetOutput):
	pass

class RunsList(SheetOutput):
	pass

class FeedOutput(SheetOutput):
	pass