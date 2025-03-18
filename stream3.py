import streamlit as st
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes untuk akses Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Upload credentials.json melalui Streamlit
uploaded_file = st.file_uploader("Upload credentials.json", type="json")
if uploaded_file is not None:
    with open("credentials.json", "wb") as f:
        f.write(uploaded_file.getbuffer())

# Fungsi untuk autentikasi Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists("credentials.json"):
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

# Fungsi untuk mengambil daftar email berdasarkan query
def list_messages(service, query=""):
    try:
        results = service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])
        return messages
    except Exception as error:
        st.error(f"Terjadi kesalahan: {error}")
        return []

# Fungsi untuk membaca isi email
def get_email_content(service, msg_id):
    try:
        msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        return subject
    except Exception as error:
        st.error(f"Terjadi kesalahan: {error}")
        return "Error"

# Main aplikasi Streamlit
def main():
    st.title("📩 Gmail API - Streamlit App")
    
    if uploaded_file is None:
        st.warning("⚠️ Silakan upload file credentials.json terlebih dahulu.")
        return
    
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    
    query = st.text_input("Masukkan kata kunci pencarian email:")
    
    if st.button("Cari Email"):
        emails = list_messages(service, query)
        if emails:
            st.write("📌 **Hasil Pencarian:**")
            for email in emails[:5]:  # Hanya menampilkan 5 email pertama
                subject = get_email_content(service, email["id"])
                st.write(f"- **{subject}**")
        else:
            st.write("❌ Tidak ada email yang ditemukan.")

if __name__ == "__main__":
    main()
