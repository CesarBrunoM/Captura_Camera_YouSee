import os
import json
import tempfile
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from logger import logger

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    credentials_data = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_cred_file:
        json.dump(credentials_data, temp_cred_file)
        temp_cred_file.flush()
        flow = InstalledAppFlow.from_client_secrets_file(temp_cred_file.name, SCOPES)
        creds = flow.run_local_server(port=0)

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='video/x-msvideo')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    logger.info(f"Arquivo enviado para o Drive com ID: {file.get('id')}")