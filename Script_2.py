import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd

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

def count_children(service, folder_id):
    num_files = 0
    num_folders = 0
    page_token = None

    while True:
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query,
            fields="files(id, mimeType), nextPageToken",
            pageToken=page_token
        ).execute()

        items = results.get('files', [])
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                num_folders += 1
                child_files, child_folders = count_children(service, item['id'])
                num_files += child_files
                num_folders += child_folders
            else:
                num_files += 1

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return num_files, num_folders

def report_folders(service, root_folder_id):
    initial_query = f"'{root_folder_id}' in parents"
    initial_root_folders = service.files().list(
        q=initial_query,
        fields="files(id, name)",
    ).execute()

    report_data = []

    for folder in initial_root_folders.get('files', []):
        folder_id = folder['id']
        folder_name = folder['name']
        print(f"Counting for folder: {folder_name} (ID: {folder_id})")
        num_files, num_folders = count_children(service, folder_id)
        
        report_data.append((folder_id, folder_name, num_folders, num_files))
        print(f"  - Total files: {num_files}")
        print(f"  - Total folders: {num_folders}")
        print('----------------------------------------------------------------------')

    export_to_excel(report_data)

def export_to_excel(report_data):
    df = pd.DataFrame(report_data, columns=['Folder ID/File ID', 'Name', 'Number of Child Folders', 'Number of Child Files'])
    df.to_excel('./Results/script_2_report_test.xlsx', index=False, engine='openpyxl')

def main():
    root_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    service = authenticate()
    report_folders(service, root_folder_id)

if __name__ == '__main__':
    main()
