import streamlit as st

# Gambar atau ikon untuk mempercantik tampilan
st.image("https://www.example.com/icon.png", width=50)

# Menampilkan metrik dengan desain lebih menarik
st.metric(label="Profit", value="$15,000", delta="+25%", delta_color="inverse")
st.metric(label="New Users", value="850", delta="-5%", delta_color="normal")
