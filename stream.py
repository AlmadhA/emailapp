import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os
import gdown
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objs as go
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from matplotlib.colors import LinearSegmentedColormap, to_hex

st.set_page_config(layout="wide")
def download_file_from_github(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved to {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def list_files_in_directory(dir_path):
    # Fungsi untuk mencetak semua isi dari suatu direktori
    for root, dirs, files in os.walk(dir_path):
        st.write(f'Direktori: {root}')
        for file_name in files:
            st.write(f'  - {file_name}')

# URL file model .pkl di GitHub (gunakan URL raw dari file .pkl di GitHub)
url = 'https://raw.githubusercontent.com/Analyst-FPnA/Dashboard-Promix/main/daftar_gudang.csv'

# Path untuk menyimpan file yang diunduh
save_path = 'daftar_gudang.csv'

# Unduh file dari GitHub
download_file_from_github(url, save_path)

def download_file_from_google_drive(file_id, dest_path):
    if not os.path.exists(dest_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest_path, quiet=False)
        
file_id = '14a4HmKACWics1ObPevlF0BXG1gVFShn_'
dest_path = f'downloaded_file.zip'
download_file_from_google_drive(file_id, dest_path)

if 'df_item' not in locals():
    with zipfile.ZipFile(f'downloaded_file.zip', 'r') as z:
        df_mie = []
        for file_name in z.namelist():
          # Memeriksa apakah file tersebut berformat CSV
            if file_name.startswith('df_sales'):
                with z.open(file_name) as f:
                    df_mie.append(pd.read_csv(f))
        # Menggabungkan semua DataFrame menjadi satu
        df_mie = pd.concat(df_mie, ignore_index=True)
        
st.title('Dashboard - Promix (WEBSMART)')

days_in_month = {
    'January': 31,
    'February': 28,  # untuk tahun non-kabisat
    'March': 31,
    'April': 30,
    'May': 31,
    'June': 30,
    'July': 31,
    'August': 31,
    'September': 30,
    'October': 31,
    'November': 30,
    'December': 31
}

df_days = pd.DataFrame([days_in_month]).T.reset_index().rename(columns={'index':'BULAN',0:'days'})
df_days['BULAN'] = df_days['BULAN']+' 2023'
df_days2 = df_days.copy()
df_days2['BULAN'] = df_days2['BULAN'].str.replace('2023','2024')
df_days = pd.concat([df_days,df_days2]) 
df_days.loc[df_days[df_days['BULAN']=='February 2024'].index,'days'] = 29

df_mie = df_mie.groupby(['BULAN','CABANG','Nama Cabang'])[['Kuantitas']].sum().reset_index()
df_mie['Tanggal'] = pd.to_datetime(df_mie['BULAN'], format='%B %Y')
df_mie['BULAN'] = pd.Categorical(df_mie['BULAN'], categories=df_mie.sort_values('Tanggal')['BULAN'].unique(), ordered=True)
df_mie = df_mie[df_mie['BULAN']>='January 2024']
pivot1=df_mie.pivot(index='Nama Cabang', columns='BULAN', values='Kuantitas').reset_index().fillna(0)

pivot1.iloc[:,1:] = pivot1.iloc[:,1:].astype('int')

def create_white_to_red_cmap():
    pastel_cmap = LinearSegmentedColormap.from_list(
        "white_red",
        [(0, (1.0, 1.0, 1.0)),  # Putih
         (1, (1.0, 0.5, 0.5))]  # Merah pastel
    )
    return pastel_cmap

def row_gradient_colors(row, cmap):
    vmin, vmax = row.min(), row.max()  # Nilai min dan max dalam satu baris
    colors = [get_color(value, vmin, vmax, cmap) for value in row]
    return colors

def get_color(value, vmin, vmax, cmap):
    norm_value = (value - vmin) / (vmax - vmin) if vmax > vmin else 0
    rgba_color = cmap(norm_value)  # Ambil warna dari colormap
    return to_hex(rgba_color)      # Konversi ke HEX


gb = GridOptionsBuilder.from_dataframe(pivot1)
gb.configure_column(pivot1.columns[0], pinned="left")
gb.configure_default_column(resizable=True)
gb.configure_grid_options(domLayout='normal')  # Menyesuaikan tinggi tabel
#gb.configure_default_column(filterable=True, sortable=True)
gb.configure_column(pivot1.columns[0], filter="text")

cmap = create_white_to_red_cmap()

row_colors = pivot1.iloc[:, 1:].apply(lambda row: row_gradient_colors(row, cmap), axis=1)


# Menambahkan cellStyle untuk setiap kolom numerik
for col_idx, col in enumerate(pivot1.columns[1:]):
    gb.configure_column(
        col,
        cellStyle=JsCode(f"""
        function(params) {{
            const colors = {row_colors.apply(lambda x: x[col_idx]).tolist()};
            return {{
                'backgroundColor': colors[params.node.rowIndex],
                'color': 'black',
                'textAlign': 'center'
            }};
        }}
        """)
    )

for col in pivot1.columns[1:]:
    gb.configure_column(col, width=150)
    
grid_options = gb.build()

AgGrid(
    pivot1,
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    height=400,
)
st.dataframe(pivot1.fillna(0), use_container_width=True, hide_index=True)
total = pd.DataFrame((pivot1.iloc[:,1:].sum(axis=0).values).reshape(1,len(pivot1.columns)-1),columns=pivot1.columns[1:])
total['Nama Cabang'] ='TOTAL'
st.dataframe(total.loc[:,[total.columns[-1]]+total.columns[:-1].to_list()], use_container_width=True, hide_index=True)
df_mie3 = df_mie.merge(df_days, how='left')
#df_mie3['AVG_SALES'] = df_mie3['QTY'] / df_mie3['days'] 
df_mie3['AVG_SALES(-Cancel nota)'] = df_mie3['Kuantitas'] / df_mie3['days'] 

df_mie3['Tanggal'] = pd.to_datetime(df_mie3['BULAN'], format='%B %Y')
df_mie3['BULAN'] = pd.Categorical(df_mie3['BULAN'], categories=df_mie3.sort_values('Tanggal')['BULAN'].unique(), ordered=True)

pivot1 = df_mie3[(df_mie3['BULAN'].str.contains('2024')) & (df_mie3['Kuantitas']>0)].pivot(index='CABANG',columns='BULAN',values='AVG_SALES(-Cancel nota)').reset_index()
total = pd.DataFrame((pivot1.iloc[:,1:].mean(axis=0).values).reshape(1,len(pivot1.columns)-1),columns=pivot1.columns[1:])
total['CABANG']='AVG DAILY'+(pivot1['CABANG'].str.len().max()+22)*' '

st.dataframe(total.loc[:,[total.columns[-1]]+total.columns[:-1].to_list()], use_container_width=True, hide_index=True)

df_mie = df_mie.merge(df_days, how='left')
df_mie['AVG_SALES(-Cancel nota)'] = df_mie['Kuantitas'] / df_mie['days'] 

df_mie2 = df_mie[df_mie['Kuantitas']!=0].groupby('BULAN')[['Nama Cabang']].nunique().rename(columns={'Nama Cabang':'Total Cabang'}).reset_index().merge(df_mie[df_mie['AVG_SALES(-Cancel nota)']>=4400].groupby(['BULAN'])[['Nama Cabang']].nunique().reset_index().rename(columns={'Nama Cabang':'Total Cabang Achieve'}), how='left'    
)
df_mie2['%'] = round((df_mie2['Total Cabang Achieve'] / df_mie2['Total Cabang']) *100,2)

df_mie2 = df_mie2[df_mie2['BULAN'].str.contains('2024')]

df_mie2['Tanggal'] = pd.to_datetime(df_mie2['BULAN'], format='%B %Y')
df_mie2['BULAN'] = pd.Categorical(df_mie2['BULAN'], categories=df_mie2.sort_values('Tanggal')['BULAN'].unique(), ordered=True)
df_mie2 = df_mie2.sort_values('BULAN').T
df_mie2.columns = df_mie2.iloc[0,:]
st.dataframe(df_mie2.iloc[[1,2,3],:].reset_index().rename(columns={'index':'BULAN'}), use_container_width=True, hide_index=True)
