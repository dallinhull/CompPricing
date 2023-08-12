import time
import gspread
from gspread import *
from oauth2client.service_account import ServiceAccountCredentials
import CareFreeHomesCrawler
from apiclient import discovery
from httplib2 import Http

# Replace with the ID of your Google Sheets file
SPREADSHEET_ID = '1_uDz-yIHdN_-H3dZf2PGEVh69vme_TX1nxlxzADyzqA'

# Replace with the name of the worksheet you want to write data to
WORKSHEET_NAME = 'CareFreeHomes'

# Authorize the API client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\dalli\OneDrive\Desktop\credentials.json', SCOPE)
client = gspread.authorize(creds)

# Formatting
SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

# Open the worksheet
worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

data = CareFreeHomesCrawler.carefree_full_list

cell_list = worksheet.range('A1:AA1000')

# Freeze top two rows
worksheet.freeze(rows=2)

reqs = {'requests': [
            {'updateSheetProperties': {
                'properties': {'gridProperties': {'frozenRowCount': 2}},
                'fields': 'gridProperties.frozenRowCount',}},
            {'repeatCell': {
                'range': {'endRowIndex': 2},
                'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                'fields': 'userEnteredFormat.textFormat.bold',}}
]}


SHEETS.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=reqs).execute()

def post_values(worksheet, data):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            cell = worksheet.cell(row_index + 3, col_index + 1)
            print(f'{cell} initialized')
            cell.value = value
            print(f'{cell} completed')
            time.sleep(1)
            worksheet.update_cell(row_index + 3, col_index + 1, cell.value)
        

# worksheet.update_cells(cell_list)
post_values(worksheet, data)
print("Finished")