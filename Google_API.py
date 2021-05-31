from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1bz115b4PJYNKSJKzwqp5uhhHxNrVt8Wmlt62s2QlvnM"
SAMPLE_RANGE_NAME = "MAIN!A:A"

def main(in_spreadsheet_id = "", in_range = SAMPLE_RANGE_NAME, data_in = []):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        #if creds and creds.expired and creds.refresh_token:
        if creds:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    ### START HERE
    #TODO: support spreadsheet ID, multiple pages for clients, etc
    #TODO: clear spreadsheet and rewrite, or append?

    values = data_in
    #values = data_in[0:4]
    
    body = {
    	"values": values
    }
    sheet.values().clear(spreadsheetId=in_spreadsheet_id, range="MAIN!A:V").execute()
    result = sheet.values().append(spreadsheetId=in_spreadsheet_id, range=in_range, valueInputOption = "RAW", body = body).execute()
    return result
    
if __name__ == '__main__':
    main()