import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards


import streamlit as st
from datetime import datetime

# Menampilkan header
st.title("Pilih Bulan dan Tahun")

# Mengatur format bulan dan tahun
today = datetime.today()
current_year = today.year
current_month = today.month

# Pilihan untuk bulan/tahun awal
start_date = st.date_input("Pilih Bulan/Tahun Awal", min_value=datetime(current_year-10, 1, 1), max_value=datetime(current_year, current_month, 1))
# Pilihan untuk bulan/tahun akhir
end_date = st.date_input("Pilih Bulan/Tahun Akhir", min_value=start_date, max_value=datetime(current_year, current_month, 1))

# Mengambil bulan dan tahun dari input pengguna
start_month_year = f"{start_date.month:02d}/{start_date.year}"
end_month_year = f"{end_date.month:02d}/{end_date.year}"

# Menampilkan hasil pilihan bulan dan tahun
st.write(f"Bulan/Tahun Awal: {start_month_year}")
st.write(f"Bulan/Tahun Akhir: {end_month_year}")

