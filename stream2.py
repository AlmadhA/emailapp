import streamlit as st
import time

# Menampilkan progress bar
st.write("Loading metrics...")

progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.1)  # Simulasi delay
