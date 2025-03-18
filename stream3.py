import streamlit as st
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# ---- KONFIGURASI ----
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = "credentials.json"

# ---- FUNGSI AUTENTIKASI ----
def authenticate_gmail():
    creds = None

    # 1️⃣ Gunakan secrets jika ada (untuk Streamlit Cloud)
    if "gmail_credentials" in st.secrets:
        credentials_dict = json.loads(st.secrets["gmail_credentials"])
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials_dict, f)

    # 2️⃣ Gunakan file credentials.json jika diunggah (untuk lokal)
    uploaded_file = st.file_uploader("Upload credentials.json", type="json")
    if uploaded_file is not None:
        with open(CREDENTIALS_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # 3️⃣ Autentikasi Gmail API
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

# ---- FUNGSI MENGAMBIL EMAIL ----
def list_messages(service, query=""):
    try:
        results = service.users().messages().list(userId="me", q=query).execute()
        return results.get("messages", [])
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return []

def get_email_subject(service, msg_id):
    try:
        msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        return subject
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return "Error"

# ---- APLIKASI STREAMLIT ----
def main():
    st.title("📩 Gmail API - Streamlit App")

    # 1️⃣ Autentikasi
    creds = authenticate_gmail()
    if creds is None:
        st.error("❌ Gagal autentikasi! Harap upload credentials.json atau atur secrets di Streamlit Cloud.")
        return
    
    service = build("gmail", "v1", credentials=creds)

    # 2️⃣ Input pencarian email
    query = st.text_input("Masukkan kata kunci pencarian email:")

    if st.button("Cari Email"):
        emails = list_messages(service, query)
        if emails:
            st.write("📌 **Hasil Pencarian:**")
            for email in emails[:5]:  # Hanya tampilkan 5 email pertama
                subject = get_email_subject(service, email["id"])
                st.write(f"- **{subject}**")
        else:
            st.write("❌ Tidak ada email yang ditemukan.")

if __name__ == "__main__":
    main()
