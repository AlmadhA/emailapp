import folium
import pandas as pd
import json
from urllib.request import urlopen
# Contoh DataFrame yang berisi nama provinsi dan rata-rata harga
data = {
    'Provinsi': ['JAWA BARAT', 'JAWA TIMUR', 'Bali', 'Sumatera Utara', 'DKI Jakarta'],
    'Rata-rata Harga': [15000, 12000, 18000, 14000, 20000]
}
df = pd.DataFrame(data)

# Membaca file GeoJSON provinsi Indonesia
# Pastikan Anda memiliki file GeoJSON yang sesuai dengan data provinsi Indonesia
with urlopen('https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-province.json?raw=true') as response:
    geojson_data = json.load(response)

# Inisialisasi peta
m = folium.Map(location=[-2.5, 118], zoom_start=5)

# Menambahkan choropleth dengan data harga
folium.Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=df,
    columns=['Provinsi', 'Rata-rata Harga'],
    key_on='properties.Propinsi',  # Sesuaikan dengan nama properti di GeoJSON
    fill_color='YlOrRd',  # Warna gradient
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Rata-rata Harga Barang',
).add_to(m)

# Menambahkan kontrol layer
folium.LayerControl().add_to(m)

# Menyimpan peta ke file HTML
m.save('peta_harga_barang_indonesia.html')
