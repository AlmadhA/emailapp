import streamlit as st

# Menampilkan metrik dengan HTML untuk warna dan styling tambahan
st.markdown("""
    <style>
        .metric-value {
            font-size: 30px;
            color: #FF6347;
        }
        .metric-label {
            font-size: 20px;
            color: #4682B4;
        }
    </style>
    <div class="metric-label">Revenue</div>
    <div class="metric-value">$10,000</div>
""", unsafe_allow_html=True)
