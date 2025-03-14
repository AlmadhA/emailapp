import streamlit as st
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import google_auth_oauthlib
import os
import requests


    
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
def authenticate_google_sheets():
    auth_code = st.query_params.get("code")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", # replace with you json credentials from your google auth app
        scopes=SCOPES
    )
    if auth_code:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        st.session_state["google_auth_code"] = auth_code
        st.session_state['creds'] = credentials
        return st.session_state['creds']

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
