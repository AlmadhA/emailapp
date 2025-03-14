
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
