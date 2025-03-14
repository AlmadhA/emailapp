
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
import google_auth_oauthlib

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
        'credentials_shopee.json', # replace with you json credentials from your google auth app
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri='http://localhost:8080/'
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
            creds = flow.run_local_server(port=8081)
        
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
