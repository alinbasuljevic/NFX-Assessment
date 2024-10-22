import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate():
    """Authenticate and return the Google Drive service."""
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

def copy_file(service, file_id, destination_folder_id):
    copied_file = {'name': '', 'parents': [destination_folder_id]}
    service.files().copy(fileId=file_id, body=copied_file).execute()

def copy_folder_contents(service, source_folder_id, destination_folder_id):
    query = f"'{source_folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            new_folder_metadata = {
                'name': item['name'],
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [destination_folder_id]
            }
            new_folder = service.files().create(body=new_folder_metadata, fields='id').execute()
            new_folder_id = new_folder.get('id')

            copy_folder_contents(service, item['id'], new_folder_id)
        else:
            copy_file(service, item['id'], destination_folder_id)

def main():
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    destination_folder_id = '1YbCxApvmj961kuV05UKqCtPP6dWIbVVe'
    service = authenticate()

    copy_folder_contents(service, source_folder_id, destination_folder_id)
    print(f"Copied contents from folder ID: {source_folder_id} to folder ID: {destination_folder_id}")

if __name__ == '__main__':
    main()
