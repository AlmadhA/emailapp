import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

add_page_title()

show_pages(
    [   
        Page("https://dashboard-harga-barang.streamlit.app/", "DE Zoomcamp", "💻"),

        # # 2024 Content
        Section("DE Zoomcamp 2024", "🧙‍♂️"),
        Page("https://dashboard-harga-barang.streamlit.app/", "📚", in_section=True),
        Page("https://dashboard-safetystock.streamlit.app/", "Module 1 Introduction & Prerequisites", "1️⃣", in_section=True)])


