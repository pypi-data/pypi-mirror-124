import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import pandas as pd


class GSheetsHelper:

    def __init__(self):
        self.scopes = None
        self.credentials_path = None

    def __init__(self, scopes, credentials_path):
        self.scopes = scopes
        self.credentials_path = credentials_path
        self.credential_dir_path = os.path.dirname(os.path.abspath(credentials_path))
        # print(self.credential_dir_path)
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.credential_dir_path + '/token.json'):
            creds = Credentials.from_authorized_user_file(self.credential_dir_path + '/token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credential_dir_path + '/credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.credential_dir_path + '/token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        self.sheet_service = service.spreadsheets()

    def get_sheet_data(self, spreadsheet_id, range_name):
        result = self.sheet_service.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            return values

    def get_auth_token(self):
        with open(self.credential_dir_path + '/token.json') as f:
            data = json.load(f)
            token = data["token"]
            # print(token)
            return token

    def get_matching_rows(self, spreadsheet_id, range_name, column_to_search, string_to_search, columns):
        r = self.get_sheet_data(spreadsheet_id, range_name)
        result_set = pd.DataFrame(r, columns=columns)
        match_rows_set = result_set[result_set[column_to_search] == string_to_search].index

        return match_rows_set

    # Delete only 1 row
    def delete_row_matching_row(self, spreadsheet_id, sheet_id, single_row_index):
        request_body = {
            'requests': [
                {
                    'deleteDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'ROWS',
                            'startIndex': single_row_index,
                            'endIndex': single_row_index + 1
                        }
                    }
                }
            ]
        }
        self.sheet_service.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request_body
        ).execute()

    def append_row_to_sheet(self, spreadsheet_id, range_name, body):
        result = self.sheet_service.values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
