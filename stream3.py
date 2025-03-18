import streamlit as st
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ---- KONFIGURASI ----
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = "token.json"

# ---- FUNGSI AUTENTIKASI ----
def authenticate_gmail():
    creds = None
    
    # 1️⃣ Gunakan credentials dari Streamlit Secrets
    if "gmail" in st.secrets:
        credentials_dict = {
            "web": {
                "client_id": st.secrets["gmail"]["client_id"],
                "client_secret": st.secrets["gmail"]["client_secret"],
                "project_id": st.secrets["gmail"]["project_id"],
                "auth_uri": st.secrets["gmail"]["auth_uri"],
                "token_uri": st.secrets["gmail"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["gmail"]["auth_provider_x509_cert_url"],
                "redirect_uris": st.secrets["gmail"]["redirect_uris"]
            }
        }
        
        # Simpan sementara ke file JSON (karena Google API butuh file)
        CREDENTIALS_FILE = "credentials_temp.json"
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials_dict, f)
        
        # 2️⃣ Autentikasi Gmail API
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Simpan token agar tidak perlu login ulang
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        
        return creds
    
    else:
        st.error("❌ Kredensial Gmail tidak ditemukan! Harap atur `secrets.toml` di Streamlit Cloud.")
        return None

# ---- FUNGSI MENGAMBIL EMAIL ----
def list_messages(service, query=""):
    try:
        results = service.users().messages().list(userId="me", q=query).execute()
        return results.get("messages", [])
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")
        return []

def get_email_subject(service, msg_id):
    try:
        msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        return subject
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")
        return "Error"

# ---- APLIKASI STREAMLIT ----
def main():
    st.title("📩 Gmail API - Streamlit App (Secrets)")

    # 1️⃣ Autentikasi Gmail API
    creds = authenticate_gmail()
    if creds is None:
        return
    
    service = build("gmail", "v1", credentials=creds)

    # 2️⃣ Input pencarian email
    query = st.text_input("🔎 Masukkan kata kunci pencarian email:")

    if st.button("Cari Email"):
        emails = list_messages(service, query)
        if emails:
            st.write("📌 **Hasil Pencarian:**")
            for email in emails[:5]:  # Hanya tampilkan 5 email pertama
                subject = get_email_subject(service, email["id"])
                st.write(f"📧 **Subject:** {subject}")
        else:
            st.warning("⚠️ Tidak ada email yang ditemukan.")

if __name__ == "__main__":
    main()
