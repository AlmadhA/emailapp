import streamlit as st
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# ---- Ambil kredensial dari secrets ----
if "google" in st.secrets:
    creds_dict = {
        "client_id": st.secrets["google"]["client_id"],
        "client_secret": st.secrets["google"]["client_secret"],
        "token_uri": st.secrets["google"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"]
    }
    creds = Credentials.from_authorized_user_info(creds_dict)
else:
    st.error("❌ Kredensial Gmail tidak ditemukan! Harap atur secrets di Streamlit Cloud.")
    st.stop()

# ---- Buat layanan Gmail ----
service = build("gmail", "v1", credentials=creds)
st.success("✅ Autentikasi berhasil!")

# ---- Ambil email ----
def get_email_subject(service, msg_id):
    try:
        msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        return subject
    except Exception as e:
        return f"Error: {e}"

st.title("📩 Gmail API - Streamlit App")

query = st.text_input("Masukkan kata kunci pencarian email:")
if st.button("Cari Email"):
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    for msg in messages[:5]:
        subject = get_email_subject(service, msg["id"])
        st.write(f"📧 **{subject}**")
