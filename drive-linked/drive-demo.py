import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file google-cloud-token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1WsuS_2tOo0iMiVDOquAd21RbzuyYQ0UaWqTwNcfD_jU'
SAMPLE_RANGE_NAME = 'Restaurants!A1:I'

creds = None
# The file google-cloud-token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('google-cloud-token.pickle'):
    with open('google-cloud-token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'google-cloud-creds.json', SCOPES)
        creds = flow.run_console()
    # Save the credentials for the next run
    with open('google-cloud-token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, includeGridData=True).execute()

print(result)
