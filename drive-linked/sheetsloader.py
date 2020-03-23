# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# If modifying these scopes, delete the file google-cloud-token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1WsuS_2tOo0iMiVDOquAd21RbzuyYQ0UaWqTwNcfD_jU'
SAMPLE_RANGE_NAME = 'Restaurants!A1:I'

def load_spreadsheet(spreadsheet_id):
    # creds = None
    # if os.path.exists('google-cloud-token.pickle'):
    #     with open('google-cloud-token.pickle', 'rb') as token:
    #         creds = pickle.load(token)

    # if not creds or not creds.valid:
    #     print("***STOP: No credentials or credentials invalid")
    #     return None

    # service = build('sheets', 'v4', credentials=creds)
    # sheet = service.spreadsheets()
    # result = sheet.get(spreadsheetId=spreadsheet_id, includeGridData=True, fields="sheets(properties,data.rowData.values(userEnteredValue,effectiveValue,hyperlink,textFormatRuns))").execute()
    # return result
    return eval(open('sheet_example.py', 'r').read())

def get_sheet(spreadsheet, name):
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == name:
            break
    else:
        raise IndexError(name)

    data = []
    for row in sheet['data'][0]['rowData']:
        if row:
            data.append(row['values'])
        else:
            data.append([])

    return data

def format_as_html(text, runs):
    built = ""
    bold = False


d=get_sheet(load_spreadsheet(SAMPLE_SPREADSHEET_ID), "Restaurants")
# print(load_spreadsheet(SAMPLE_SPREADSHEET_ID))