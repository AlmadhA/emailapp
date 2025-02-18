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
with urlopen('https://github.com/superpikar/indonesia-geojson/blob/master/indonesia-province.json?raw=true') as response:
    geojson_data = json.load(response)
geojson_data

