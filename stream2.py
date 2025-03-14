
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

from StreamlitGauth.google_auth import Google_auth

client_id = "1036706857790-jdp1lg4u2j5a99rg9q0rtsv2hg9ultt9.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "http://localhost:8501"

login = Google_auth(clientId=client_id, 
 clientSecret=client_secret,redirect_uri=redirect_uri
 )

if login == "authenticated":
   print('heloo')
   pass
