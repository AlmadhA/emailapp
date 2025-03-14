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

def ls_get(k, key=None):
    return st_js_blocking(f"return JSON.parse(localStorage.getItem('{k}'));", key)


def ls_set(k, v, key=None):
    jdata = json.dumps(v, ensure_ascii=False)
    st_js_blocking(f"localStorage.setItem('{k}', JSON.stringify({jdata}));", key)

def init_session():
    user_info = ls_get("user_info")
    if user_info:
        st.session_state["user_info"] = user_info

def auth_flow():
    st.write("Welcome to My App!")
    auth_code = st.query_params.get("code")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', # replace with you json credentials from your google auth app
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_url='http://localhost:8080/'
    )
    if auth_code:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        st.write("Login Done")
        user_info_service = build(
            serviceName="oauth2",
            version="v2",
            credentials=credentials,
        )
        user_info = user_info_service.userinfo().get().execute()
        assert user_info.get("email"), "Email not found in infos"
        st.session_state["google_auth_code"] = auth_code
        st.session_state["user_info"] = user_info
        ls_set("user_info", user_info)
        # TODO fix calling consecutive ls_set is not working 
        # ls_set("google_auth_code", auth_code)
    else:
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )
        st.link_button("Sign in with Google", authorization_url)

def main():
    init_session()
    if "user_info" not in st.session_state:
        auth_flow()

    if "user_info" in st.session_state:
        main_flow()

if __name__ == "__main__":
    main()

    
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
