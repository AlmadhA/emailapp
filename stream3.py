import folium
import pandas as pd
import json
from urllib.request import urlopen
import requests
# Contoh DataFrame yang berisi nama provinsi dan rata-rata harga
data = {
    'Provinsi': ['JAWA BARAT', 'JAWA TIMUR'],
    'Rata-rata Harga': [15000, 12000]
}
df = pd.DataFrame(data)

# Membaca file GeoJSON provinsi Indonesia
# Pastikan Anda memiliki file GeoJSON yang sesuai dengan data provinsi Indonesia

#geojson_data = pd.DataFrame(requests.get('https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-province.json').json())
# Inisialisasi peta
m = folium.Map(location=[-0.4471383, 117.1655734], zoom_start=3)
#geojson_data
# Menambahkan choropleth dengan data harga
folium.Choropleth(
    geo_data='https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-province.json',
    name='choropleth',
    data=df,
    columns=['Provinsi', 'Rata-rata Harga'],
    key_on='feature.properties.Propinsi',  # Sesuaikan dengan nama properti di GeoJSON
    fill_color='YlOrRd',  # Warna gradient
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Rata-rata Harga Barang',
).add_to(m)

# Menambahkan kontrol layer
folium.LayerControl().add_to(m)

# Menyimpan peta ke file HTML
#m.save('peta_harga_barang_indonesia.html')
