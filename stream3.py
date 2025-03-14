import streamlit as st
import pandas as pd
import os
import base64
import mimetypes
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

from auth0_component import login_button
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

clientId = 'QwBaicViCKun5FgmCL5l9gWGzDlsjEgp'
domain = 'dev-oee4zt3daq2ov6tp.us.auth0.com'

clientId = os.environ[clientId]
domain = os.environ[domain]

st.title('Welcome to Auth0-Streamlit')

with st.echo():
    user_info = login_button(clientId=clientId, domain=domain)
    if user_info:
        st.write(f'Hi {user_info["nickname"]}')
        # st.write(user_info) # some private information here
        
if not user_info:
    st.write("Please login to continue")
    
# Jika memodifikasi scope, hapus file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail(file_json):
    """Authenticate and return Gmail API service."""
    creds = None
    # Token file untuk menyimpan kredensial yang telah diakses sebelumnya.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Jika tidak ada kredensial yang valid, lakukan login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                file_json, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Simpan kredensial untuk penggunaan berikutnya
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Membangun layanan Gmail API
    try:
        service = build('gmail', 'v1', credentials=creds)
        st.write(service)
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

#service = authenticate_gmail(file_json = 'credentials_shopee.json')
keywords_gojek = ['Mie Gacoan, Batu Tulis','Mie Gacoan, Cibubur','Mie Gacoan, Daan Mogot','Mie Gacoan, Kemang Raya','Mie Gacoan, Tebet',
            'Mie Gacoan, Padalarang','Mie Gacoan, Manukan','Mie Gacoan, Jatinangor','Mie Gacoan, Semarang Brigjen Sudiarto', 'Mie Gacoan, Mangga Besar']
keywords_shopee = ['Shopee food - Mie Gacoan - Batu Tulis','Shopee food - Mie Gacoan - Cibubur','Shopee food - Mie Gacoan - Daan Mogot','Shopee food - Mie Gacoan - Kemang Raya','Shopee food - Mie Gacoan - Tebet',
            'Shopee food - Mie Gacoan - Padalarang','Shopee food - Mie Gacoan - Manukan','Shopee food - Mie Gacoan - Jatinangor','Shopee food - Mie Gacoan - Semarang Brigjen Sudiarto', 'Shopee food - Mie Gacoan - Mangga Besar']
cab = ['BGRBAT','BKSALT','GGPDAA','KYBKEM','KYBTEB','NPHCIB','SBYTAN','SMDJAT','SMGSUD','TNAMAN']
for i,query in enumerate(keywords_shopee):
    messages = list_messages(service, query)
    if messages:
        st.write(f'Found {len(messages)} messages.')
        for msg in messages[:7]:
            msg_id = msg['id']
            save_attachment(service, msg_id, store_dir=f'downloads/{cab[i]}')
    else:
        print('No messages found with the given criteria.')
