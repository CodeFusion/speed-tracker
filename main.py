import math
import os
import pickle

import speedtest
from datetime import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def perform_speedtest():
    servers = [os.getenv('SPEEDTEST_SERVER_ID')]
    st = speedtest.Speedtest()
    st.get_servers(servers)
    st.get_best_server()
    st.download()
    st.upload()
    return st.results.dict()


def send_to_sheet(latency, download, upload):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    sheet_range = os.getenv('SHEET_RANGE')
    creds = None
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes
            )
            creds = flow.run_local_server(port=7765)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    values = [
        [timestamp, latency, download, upload]
    ]
    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=sheet_range,
        body=body, valueInputOption='USER_ENTERED'
    ).execute()

    print('{0} cells appended.'.format(result
                                       .get('updates')
                                       .get('updatedCells')))


if __name__ == '__main__':
    load_dotenv('.env')
    results = perform_speedtest()
    download = round(results['download']/1000000, 2)
    upload = round(results['upload']/1000000, 2)
    latency = math.ceil(results['ping'])
    print('Download: ' + str(download) + 'Mbps')
    print('Upload: ' + str(upload) + 'Mbps')
    print('Ping: ' + str(latency) + 'ms')
    send_to_sheet(latency, download, upload)



