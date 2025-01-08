import streamlit as st
import requests
def run_stream_script(url):
    # Mengunduh file dari GitHub
    response = requests.get(url)
    if response.status_code == 200:
        # Menjalankan file yang diunduh
        exec(response.text, globals())
    else:
        st.error(f"Failed to download file: {response.status_code}")

# Arahkan ke aplikasi berdasarkan pilihan pengguna
def run_lead():
    stream1_url = 'https://raw.githubusercontent.com/Analyst-FPnA/Leadtime/main/Internal.py'
    run_stream_script(stream1_url)
  
st.expander('Dashboard'):
  create_page = st.Page(run_lead, title="Create entry", icon=":material/add_circle:")
  delete_page = st.Page("stream2.py", title="Delete entry", icon=":material/delete:")
  
  pg = st.navigation([create_page, delete_page])


