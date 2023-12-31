import time
import gspread
from gspread import *
from oauth2client.service_account import ServiceAccountCredentials
import VisionaryHomesCrawler
from apiclient import discovery
from httplib2 import Http

# Replace with the ID of your Google Sheets file
SPREADSHEET_ID = '1_uDz-yIHdN_-H3dZf2PGEVh69vme_TX1nxlxzADyzqA'

# Replace with the name of the worksheet you want to write data to
WORKSHEET_NAME = 'VisionaryHomes'

# Authorize the API client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\dalli\OneDrive\Desktop\credentials.json', SCOPE)
client = gspread.authorize(creds)

# Formatting
SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

# Open the worksheet
worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

# instantiate variable and assign builder spec list
data = VisionaryHomesCrawler.visionary_full_list

# Over-specify the worksheet range that will be modified
cell_list = worksheet.range('A1:AA1000')

# Freeze top two rows
worksheet.freeze(rows=2)

# Freeze top two rows and bold top 2 rows
reqs = {'requests': [
            {'updateSheetProperties': {
                'properties': {'gridProperties': {'frozenRowCount': 2}},
                'fields': 'gridProperties.frozenRowCount',}},
            {'repeatCell': {
                'range': {'endRowIndex': 2},
                'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                'fields': 'userEnteredFormat.textFormat.bold',}}
]}

# Run the json code above for formatting
SHEETS.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=reqs).execute()

# Enumerate spec list for tuple, and enumerate spec specific info for another tuple
# Use first numerical value for column/row designation, use spec info for cell value
def post_values(worksheet, data):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            cell = worksheet.cell(row_index + 3, col_index + 1)
            print(f'{cell} initialized')
            cell.value = value
            print(f'{cell} completed')
            time.sleep(1)
            worksheet.update_cell(row_index + 3, col_index + 1, cell.value)
        

# Run it
post_values(worksheet, data)
print("Finished")