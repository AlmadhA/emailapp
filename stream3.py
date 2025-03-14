import streamlit as st
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import requests

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

# Jika memodifikasi scope, hapus file token.json

def authenticate_gmail(file_json):
    """Authenticate and return Gmail API service."""
    creds = service_account.Credentials.from_service_account_file(
        'credentials_shopee.json', scopes=SCOPES)
    
    # Membangun layanan Gmail API
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as error:
        print(f'An error occurred: {error}')
        return None
    
def list_messages(service, query):
    """List email messages based on a query."""
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
    
def get_message(service, msg_id):
    """Get a specific email message."""
    try:
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        return msg
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def save_attachment(service, msg_id, store_dir='downloads'):
    """Download attachment if it's a CSV file."""
    msg = get_message(service, msg_id)
    if not msg:
        return
    
    for part in msg['payload']['parts']:
        if 'filename' in part and part['filename']:
            file_name = part['filename']
            if file_name.endswith('.csv'):
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=msg_id, id=part['body']['attachmentId']).execute()
                data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

                if not os.path.exists(store_dir):
                    os.makedirs(store_dir)

                file_path = os.path.join(store_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(data)
                print(f'Attachment {file_name} saved to {file_path}')

