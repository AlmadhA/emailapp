import streamlit as st
import pandas as pd
import requests



stream1_url = 'https://raw.githubusercontent.com/Analyst-FPnA/Dashboard-Safety-Stock/main/stream.py'
create_page = st.Page("stream.py", title="Create entry", icon=":material/add_circle:")
delete_page = st.Page("stream2.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation(
                    create_page, delete_page], expanded=True)
pg.run()



