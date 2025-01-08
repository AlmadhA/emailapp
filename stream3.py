import streamlit as st


create_page = st.Page("stream.py", title="Create entry", icon=":material/add_circle:")
delete_page = st.Page("stream2.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([create_page, delete_page])


