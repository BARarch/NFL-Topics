import parsebot.parsebot_classes.modelGS as mgs

class ParseConfig:
	def __init__(self, name, sheet):
		self.project = name
		self.sheetId = sheet
		print('ParseConfig: Says whatch doin?')
		try:
			self.output = ParseOutput(self.project, self.sheetId)
		except Exception as e:
			print(str(e))

class ParseOutput:
	def __init__(self, name, sheetId):
		self.project = name
		self.sheetId = sheetId
		print('ParseOutput: Nothin Much.')
		self.credentials = mgs.modelInit()

	def test_write(self):
		"""Google Sheets API Code.

		Writes all team news link data from RSS feed to the NFL Team Articles speadsheet.
		https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
		"""
		credentials = get_credentials()
		http = credentials.authorize(mgs.httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = mgs.discovery.build('sheets', 'v4', http=http,
								  discoveryServiceUrl=discoveryUrl)

		spreadsheet_id = '1lJa1YVucaoDI0DW0VdyaJza8uAmvjGPdL-krRLiaMuc'
		value_input_option = 'RAW'
		rangeName = 'RUNS!A' + 2
		values = 'Hello World'
		body = {
			  'values': values
		}
		
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
														valueInputOption=value_input_option, body=body).execute()

		return result
