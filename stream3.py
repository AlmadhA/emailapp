import folium
import requests
import pandas as pd
from folium import GeoJsonTooltip
from streamlit_folium import folium_static
import streamlit as st

# Contoh DataFrame yang berisi nama provinsi dan rata-rata harga
data = {
    'City': ['MALANG', 'KEDIRI', 'SURABAYA', 'JOMBANG'],
    'Rata-rata Harga': [15000, 12000, 14000,9000]
}

df = pd.DataFrame(data)

# Buat peta
m = folium.Map(location=[-0.4471383, 117.1655734], zoom_start=5)

# Mendapatkan data geojson
if geojson_data is None:
    geojson_data = requests.get(
        "https://github.com/okzapradhana/indonesia-city-geojson/blob/master/indonesia-cities.json?raw=true"
    ).json()

# Gabungkan data GeoJSON dengan DataFrame df berdasarkan provinsi
# Asumsikan 'Name' adalah kolom di GeoJSON yang berisi nama provinsi yang sama dengan kolom di df

# Pastikan bahwa nama kolom 'City' di df sama dengan 'Name' di GeoJSON
#df['City'] = df['City'].str.title()  # Menyamakannya dengan format nama di GeoJSON

# Gabungkan df ke dalam GeoJSON berdasarkan 'City' dan 'Name'
geojson_data_with_prices = []
for feature in geojson_data['features']:
    provinsi = feature['properties']['Name']
    harga = df.loc[df['City'] == provinsi, 'Rata-rata Harga'].values
    if harga.size>0:
        feature['properties']['Rata-rata Harga'] = float(harga[0])
    else:
        feature['properties']['Rata-rata Harga'] = None
    geojson_data_with_prices.append(feature)

geojson_data['features'] = geojson_data_with_prices

# Menambahkan choropleth dengan data harga
folium.Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=df,
    columns=['City', 'Rata-rata Harga'],
    key_on='properties.Name',  # Sesuaikan dengan nama properti di GeoJSON
    fill_color='YlOrRd',  # Warna gradient
    fill_opacity=0.7,
    line_opacity=0.05,
    legend_name='Rata-rata Harga Barang',
).add_to(m)

# Menambahkan GeoJson dengan Tooltip
folium.GeoJson(
    geojson_data,
    name="City",
    tooltip=GeoJsonTooltip(
        fields=["Name", "Rata-rata Harga"],  # Sesuaikan dengan kolom yang ada pada GeoJSON
        aliases=["City:", "Rata-rata Harga:"],  # Label yang akan ditampilkan di tooltip
        localize=True
    ),
    style_function=lambda x: {
        #'fillOpacity': 0.0 if x['properties']['Rata-rata Harga'] is None else 0.7,  # Set opasitas area
        'weight': 0.2,  # Menghilangkan garis perbatasan
        'color': 'white'  # Menghilangkan warna garis perbatasan
    }
).add_to(m)
folium.TileLayer('cartodbpositron', control=False).add_to(m)
# Menambahkan kontrol layer
folium.LayerControl().add_to(m)

# Menampilkan peta

folium_static(m)

# Menyimpan peta ke file HTML
# m.save('peta_harga_barang_indonesia.html')
