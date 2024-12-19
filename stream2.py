import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards


# Menampilkan metrik dengan desain lebih menarik
st.metric(label="Profit", value="$15,000", delta="+25%", delta_color="inverse")
st.metric(label="New Users", value="850", delta="-5%", delta_color="normal")
style_metric_cards()
