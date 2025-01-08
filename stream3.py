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
stream1_url = 'https://raw.githubusercontent.com/Analyst-FPnA/Dashboard-Safety-Stock/main/stream.py'
create_page = st.Page("stream.py", title="Create entry", icon=":material/add_circle:")
delete_page = st.Page(run_stream_script(stream1_url), title="Delete entry", icon=":material/delete:")

pg = st.navigation([st.Section('Dashboard'),create_page, delete_page])
pg.run()

