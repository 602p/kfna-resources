import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from autolink import linkify

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

    service = build('sheets', 'v4')
    sheet = service.spreadsheets()
    result = sheet.get(spreadsheetId=spreadsheet_id, includeGridData=True, fields="sheets(properties,data.rowData.values(userEnteredValue,effectiveValue,effectiveFormat,hyperlink,textFormatRuns))").execute()
    return result
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

    maxwidth = max(len(r) for r in data)
    for row in data:
        row += [{}] * (maxwidth - len(row))

    return data

def get_text(cell):
    if not cell:
        return ''
    return list(cell.get('effectiveValue', {0:''}).values())[0]

def build_tags(format, closing=False):
    t = []
    if format.get('bold'):
        t.append('b')
    if format.get('italic'):
        t.append('i')
    if format.get('underline'):
        t.append('u')

    r = ""
    if closing: t.reverse()
    for tag in t:
        r += "<"+("/" if closing else "")+tag+">"

    return r

def get_html(cell):
    text = get_text(cell)
    spans = cell.get('textFormatRuns', [])
    eff = cell.get('effectiveFormat', {'textFormat':{}})['textFormat']

    if spans:
        fmt = {**eff, **spans[0]['format']}
        out = build_tags(fmt)
        spans = spans[1:]

        previdx = 0
        while spans:
            out += text[previdx:spans[0]['startIndex']]
            previdx = spans[0]['startIndex']
            out += build_tags(fmt, True)
            fmt = {**eff, **spans[0]['format']}
            out += build_tags(fmt)
            spans = spans[1:]

        out += text[previdx:]
        out += build_tags(fmt, True)
    else:
        out = build_tags(eff)
        out += text
        out += build_tags(eff, True)

    out = out.replace("\n", "<br/>")
    out = linkify(out)
    return out


d=get_sheet(load_spreadsheet(SAMPLE_SPREADSHEET_ID), "Restaurants")
# print(load_spreadsheet(SAMPLE_SPREADSHEET_ID))