import streamlit as st
from datetime import datetime

# Menampilkan judul aplikasi
st.title("Pilih Bulan dan Tahun")

# Mendapatkan tahun saat ini
current_year = datetime.today().year

# Daftar bulan dalam format singkatan (misalnya Jan, Feb, Mar, ...)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Daftar tahun (misalnya 10 tahun terakhir hingga tahun sekarang)
years = [str(i) for i in range(current_year-10, current_year+1)]

# Pilihan bulan dan tahun awal
start_month = st.selectbox("Pilih Bulan Awal", months)
start_year = st.selectbox("Pilih Tahun Awal", years)

# Pilihan bulan dan tahun akhir
end_month = st.selectbox("Pilih Bulan Akhir", months)
end_year = st.selectbox("Pilih Tahun Akhir", years)

# Menampilkan hasil dalam format %b %Y (misalnya Jan 2024)
start_date = f"{start_month} {start_year}"
end_date = f"{end_month} {end_year}"

# Menampilkan pilihan
st.write(f"Bulan/Tahun Awal: {start_date}")
st.write(f"Bulan/Tahun Akhir: {end_date}")
