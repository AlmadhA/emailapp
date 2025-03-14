import streamlit as st
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import google_auth_oauthlib
import os
import requests
from streamlit_js import st_js, st_js_blocking
import os
import base64
import mimetypes

import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request


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
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())
    
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


service = authenticate_gmail(file_json = 'credentials_shopee.json')

keywords_gojek = ['Mie Gacoan, Batu Tulis','Mie Gacoan, Cibubur','Mie Gacoan, Daan Mogot','Mie Gacoan, Kemang Raya','Mie Gacoan, Tebet',
            'Mie Gacoan, Padalarang','Mie Gacoan, Manukan','Mie Gacoan, Jatinangor','Mie Gacoan, Semarang Brigjen Sudiarto', 'Mie Gacoan, Mangga Besar']
keywords_shopee = ['Shopee food - Mie Gacoan - Batu Tulis','Shopee food - Mie Gacoan - Cibubur','Shopee food - Mie Gacoan - Daan Mogot','Shopee food - Mie Gacoan - Kemang Raya','Shopee food - Mie Gacoan - Tebet',
            'Shopee food - Mie Gacoan - Padalarang','Shopee food - Mie Gacoan - Manukan','Shopee food - Mie Gacoan - Jatinangor','Shopee food - Mie Gacoan - Semarang Brigjen Sudiarto', 'Shopee food - Mie Gacoan - Mangga Besar']
cab = ['BGRBAT','BKSALT','GGPDAA','KYBKEM','KYBTEB','NPHCIB','SBYTAN','SMDJAT','SMGSUD','TNAMAN']

for i,query in enumerate(keywords_shopee):
    messages = list_messages(service, query)
    if messages:
        print(f'Found {len(messages)} messages.')
        for msg in messages[:7]:
            msg_id = msg['id']
            save_attachment(service, msg_id, store_dir=f'downloads/{cab[i]}')
    else:
        print('No messages found with the given criteria.')

# SCOPES untuk membaca dan mengedit Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate_google_sheets():
    creds = None
    
    # Cek apakah token sudah ada dan masih valid
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Tentukan port untuk menjalankan server lokal dan membuka browser
            creds = flow.run_local_server(port=0)  # Menggunakan port 0, agar sistem memilih port yang tersedia

        # Simpan token untuk penggunaan berikutnya
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

# Fungsi untuk membaca data dari Google Sheets
def read_sheet(spreadsheet_id, range_name):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return pd.DataFrame(values)

# Fungsi untuk autentikasi pengguna berdasarkan email
def authenticate_user(email):
    access_control_df = pd.read_csv('database.csv')  # Membaca data akses
    user_access = access_control_df[access_control_df['Email'] == email]
    
    if not user_access.empty:
        return user_access['File ID'].tolist()  # Mengembalikan list ID file yang bisa diakses
    else:
        return []

# Streamlit UI
st.title('Google Sheets Access App')

# Autentikasi pengguna melalui Google
email = st.text_input("Enter your email address:")

if email:
    # Verifikasi apakah email memiliki akses ke file
    file_ids = authenticate_user(email)
    
    if file_ids:
        st.success("Access granted!")
        
        # Menampilkan sidebar dengan menu pilihan file berdasarkan email pengguna
        selected_file_id = st.sidebar.selectbox("Select a Google Sheet file", file_ids)
        
        # Membaca data dari file yang dipilih
        if selected_file_id:
            range_name = st.text_input("Enter the range (e.g., Sheet1!A1:D10):", "Sheet1!A1:D10")
            if range_name:
                sheet_data = read_sheet(selected_file_id, range_name)
                st.write(sheet_data)
    else:
        st.error("You do not have access to any sheets.")
