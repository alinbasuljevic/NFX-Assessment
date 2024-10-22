import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_and_folders(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    report_data = []
    for item in items:
        item_id = item['id']
        item_name = item['name']
        report_data.append((item_id, item_name))

    return report_data

def export_to_excel(report_data):
    df = pd.DataFrame(report_data, columns=['Folder ID/File ID', 'Name'])
    df.to_excel('./Results/script_1_report.xlsx', index=False, engine='openpyxl')

def main():
    folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    service = authenticate()
    
    report_data = list_files_and_folders(service, folder_id)

    export_to_excel(report_data)

    print(f"Exported {len(report_data)} items to script_1_report.xlsx.")

if __name__ == '__main__':
    main()
