import streamlit as st
import webbrowser
import streamlit.components.v1 as components
st.sidebar.title('Dashboard')

# Menambahkan beberapa link ke GitHub lainnya di sidebar
if st.sidebar.button('Harga Barang'):
    webbrowser.open('https://dashboard-harga-barang.streamlit.app/', new=0)
if st.sidebar.button('Safety Stock'):
    webbrowser.open('https://dashboard-safetystock.streamlit.app/', new=0)
