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
		rangeName = 'DjangoTest!E' + '2'
		values = [['hello world from django sheetoutput class and parsebot Management']]
		body = {
			  'values': values
		}
		
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
														valueInputOption=value_input_option, body=body).execute()
		return result

	def get_rows(self, rangeString):
		pass

	def output_row(self, row, rangeString):
		"""Google Sheets API Code.  Sends output to current row
		"""
		service = build('sheets', 
						'v4', 
						credentials=SheetOutput.cred.get_cred(),
						discoveryServiceUrl=SheetOutput.discoveryUrl)

		value_input_option = 'RAW'
		
		values = [row]
		body = {
			  'values': values
		}


		try:
			result = service.spreadsheets().values().update(spreadsheetId=SheetOutput.SheetUrl, range=rangeString,
														valueInputOption=value_input_option, body=body).execute()
		except:
			print('Missed Row Output')
		else:
			pass
			
		return result
		pass

	def output_rows(self, rows, rangeString):
		"""Google Sheets API Code.
		"""
		service = build('sheets', 
						'v4', 
						credentials=SheetOutput.cred.get_cred(),
						discoveryServiceUrl=SheetOutput.discoveryUrl)

		value_input_option = 'RAW'
		
		values = rows
		body = {
			  'values': values
		}

		try:
			result = service.spreadsheets().values().update(spreadsheetId=SheetOutput.SheetUrl, range=rangeString,
														valueInputOption=value_input_option, body=body).execute()
		except:
			print('Missed Row Output')
		else:
			pass
			
		return result
		

	def range_string(self, sheet, colunm, row):
		return '{}!{}{}'.format(str(sheet), str(colunm), str(row))

	def sheet_range(rangeString):
		delim = rangeString.find('!')
		sheet = rangeString[:delim]
		colunm = rangeString[delim + 1]
		row = rangeString[delim + 2:]


	def get_current_row(self, sheet):
		pass






class FeedList(SheetOutput):
	def __init__(self):
		pass

	def get_current_row():
		pass

	def set_current_row():
		pass

	def range_string():
		pass

class ExceptionList(SheetOutput):
	def __init__(self):
		pass

	def get_current_row():
		pass

	def set_current_row():
		pass

	def range_string():
		pass

class RunsList(SheetOutput):
	def __init__(self):
		pass

	def get_current_row():
		pass

	def set_current_row():
		pass

	def range_string():
		pass

class FeedOutput(SheetOutput):
	def __init__(self):
		pass

	def get_current_row():
		pass

	def set_current_row():
		pass

	def range_string():
		pass