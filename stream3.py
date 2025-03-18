import streamlit as st
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes untuk akses Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Fungsi autentikasi menggunakan Secrets
def authenticate_gmail():
    creds = None

    if "google" in st.secrets and "credentials" in st.secrets["google"]:
        credentials_json = st.secrets["google"]["credentials"]
        creds_dict = json.loads(credentials_json)
        
        # Simpan kredensial sementara untuk autentikasi
        with open("credentials.json", "w") as f:
            json.dump(creds_dict, f)

        try:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            return creds
        except Exception as e:
            st.error(f"Terjadi kesalahan saat autentikasi: {e}")
            return None
    else:
        st.warning("⚠️ Kredensial tidak ditemukan dalam Streamlit Secrets.")
        return None

# Main aplikasi Streamlit
def main():
    st.title("📩 Gmail API - Streamlit App")

    creds = authenticate_gmail()
    if creds:
        st.success("✅ Autentikasi berhasil!")
        service = build("gmail", "v1", credentials=creds)
        
        query = st.text_input("Masukkan kata kunci pencari
