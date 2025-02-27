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
from datetime import datetime
import plotly.graph_objs as go
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from matplotlib.colors import LinearSegmentedColormap, to_hex
import numpy as np
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


# Contoh data
data = {
    "Tahun": [2020, 2020, 2021, 2021],
    "Kategori": ['A', 'B', 'A', 'B'],
    "Pendapatan": [100, 150, 120, 180],
    "Biaya": [50, 60, 55, 70]
}
df = pd.DataFrame(data)

st.markdown("""
Ag-grid (not this component, which is free) has its own [licensing options](https://www.ag-grid.com/documentation/react/licensing/). If you do have an license,
you can load it though ```license_key``` parameter on grid call.  
""")


enable_enterprise = st.checkbox("Enable Enterprise Features", True)


key = "enterprise_disabled_grid"
license_key = None

if enable_enterprise:
    key = "enterprise_enabled_grid"
    license_key = license_key


data = {
    "Nama Cabang": ["Cabang A", "Cabang B", "Cabang C"],
    "Provinsi": ["Provinsi X", "Provinsi Y", "Provinsi Z"],
    "Nama Barang": ["Barang 1", "Barang 2", "Barang 3"],
    "Januari": [100, 200, 150],
    "Februari": [120, 180, 160],
    "Maret": [130, 190, 170],
}

df = pd.DataFrame(data)
go = GridOptionsBuilder.from_dataframe(df)
# Kolom yang akan dikelompokkan
go.configure_column("Nama Cabang", rowGroup=True)
#go.configure_column("Provinsi", rowGroup=True)
#go.configure_column("Nama Barang", rowGroup=True)

# Kolom yang digunakan untuk pivot
go.configure_column(field = "Januari", headerName="Januari",aggFunc="sum",)
go.configure_column(field = "Februari", headerName="Februari",aggFunc="sum")
go.configure_column(field = "Maret", headerName="Maret",aggFunc="sum")

# Tambahkan kolom baru untuk selisih antara Februari dan Maret
# Gunakan valueGetter untuk menghitung selisih antara Februari dan Maret
go.configure_column(
    "Kenaikan Feb-Mar", 
    valueGetter="data.Maret - data.Februari",
    headerName="Kenaikan Feb-Mar", aggFunc="sum"
)

go.configure_default_column(
    flex=1,
    minWidth=130,
    enableValue=True,
    enableRowGroup=True,
    enablePivot=True
)
go = go.build()
# Menambahkan pengaturan untuk auto group column (kolom grup otomatis)
go['autoGroupColumnDef'] = {
    'minWidth': 200,
    'pinned': 'left'
}

# Mengaktifkan Pivot Mode
go['pivotMode'] = False

# Membangun grid options
go['pivotPanelShow'] = "never"
AgGrid(
    df,
    go,
    enable_enterprise_modules=enable_enterprise,
    #license_key=license_key,
    #key=key,
)



def create_dual_axis_chart(data, x_column, y_bar_column, y_line_column, title):
    fig = go.Figure()

    # Menambahkan bar chart
    fig.add_trace(
        go.Bar(
            x=data[x_column],
            y=data[y_bar_column],
            name=y_bar_column,
            marker_color='#143d59',
            yaxis='y1'
        )
    )

    # Menambahkan line chart
    fig.add_trace(
        go.Scatter(
            x=data[x_column],
            y=data[y_line_column],
            name=y_line_column,
            mode='lines+markers',
            line=dict(color="#f4b41a", width=4),
            yaxis='y2'
        )
    )

    # Menyesuaikan layout untuk dua sumbu y
    fig.update_layout(
        title=title,
        xaxis=dict(title=x_column),
        yaxis=dict(
            title=y_bar_column,
            #titlefont=dict(color='#143d59'),
            tickfont=dict(color='#143d59'),
            range=[5000000, 25000000]
        ),
        yaxis2=dict(
            title=y_line_column,
            #titlefont=dict(color="#f4b41a"),
            tickfont=dict(color="#f4b41a"),
            overlaying='y',
            side='right',
            range=[130, 250]
        ),
        legend=dict(x=0.1, y=1.1, orientation='h'),
        template="plotly_white",
        margin=dict(l=50, r=50, t=40, b=40),
        paper_bgcolor="white",  # Warna background luar (canvas), termasuk margin
        plot_bgcolor="white",
        width=1150
    )
    return fig




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
df_days['BULAN'] = df_days['BULAN'].str[:3]+' 2023'
df_days2 = df_days.copy()
df_days2['BULAN'] = df_days2['BULAN'].str.replace('2023','2024')
df_days = pd.concat([df_days,df_days2]) 
df_days.loc[df_days[df_days['BULAN']=='February 2024'].index,'days'] = 29

col =  st.columns(3)
with col[0]:
    with stylable_container(
        key='title',
        css_styles="""
            {
                color:#143d59
            }
            """,
    ):
        st.write(' ')
        st.header("Dashboard - Promix (WEBSMART)")
with col[1]:
    # Mendapatkan tahun saat ini
    current_year = datetime.today().year
    # Daftar bulan dalam format singkatan (misalnya Jan, Feb, Mar, ...)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Daftar tahun (misalnya 10 tahun terakhir hingga tahun sekarang)
    years = [str(i) for i in range(current_year-10, current_year+1)]
    start_month = st.selectbox("Pilih Bulan Awal", months)    
    end_month = st.selectbox("Pilih Bulan Akhir", months)
with col[2]:
    start_year = st.selectbox("Pilih Tahun Awal", years)
    end_year = st.selectbox("Pilih Tahun Akhir", years)


        
df_mie = df_mie.groupby(['BULAN','CABANG','Nama Cabang'])[['Kuantitas']].sum().reset_index()
df_mie['Tanggal'] = pd.to_datetime(df_mie['BULAN'], format='%b-%y')
df_mie['BULAN'] = df_mie['Tanggal'].dt.strftime('%b %Y')
df_mie['BULAN'] = pd.Categorical(df_mie['BULAN'], categories=df_mie.sort_values('Tanggal')['BULAN'].unique(), ordered=True)
df_mie = df_mie[df_mie['BULAN']>='Jan 2024']
pivot1=df_mie.pivot(index='Nama Cabang', columns='BULAN', values='Kuantitas').reset_index().fillna(0)

pivot1.iloc[:,1:] = pivot1.iloc[:,1:].astype('int')

def create_white_to_red_cmap():
    yellow_cmap = LinearSegmentedColormap.from_list(
        "white_yellow",  # Nama colormap
        [(0, (1.0, 1.0, 1.0)),  # Putih (R=1.0, G=1.0, B=1.0)
         (1, (244/255, 180/255, 26/255))]  # Kuning '#f4b41a' (RGB normed value)
    )
    return yellow_cmap

def row_gradient_colors(row, cmap):
    vmin, vmax = row.min(), row.max()  # Nilai min dan max dalam satu baris
    colors = [get_color(value, vmin, vmax, cmap) for value in row]
    return colors

def get_color(value, vmin, vmax, cmap):
    norm_value = (value - vmin) / (vmax - vmin) if vmax > vmin else 0
    rgba_color = cmap(norm_value)  # Ambil warna dari colormap
    return to_hex(rgba_color)      # Konversi ke HEX


gb = GridOptionsBuilder.from_dataframe(pivot1)


cmap = create_white_to_red_cmap()

row_colors = pivot1.iloc[:, 1:].apply(lambda row: row_gradient_colors(row, cmap), axis=1)


# Menambahkan cellStyle untuk setiap kolom numerik
for col_idx, col in enumerate(pivot1.columns[1:]):
    gb.configure_column(
        col, minWidth=150, maxWidth=150,
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


#gb.configure_grid_options(suppressColumnToolPanel=True)
header_style = {'backgroundColor': '#143d59', 'color': 'white'}
for col in pivot1.columns:
    gb.configure_column(col, headerStyle=header_style)
gb.configure_column(pivot1.columns[0], pinned="left",  filter="text", cellStyle={'backgroundColor': '#143d59', 'color': 'white'})
gb.configure_default_column(resizable=True,filterable=True, sortable=True)
grid_options = gb.build()
#grid_options["domLayout"] = "autoHeight"

total = pd.DataFrame((pivot1.iloc[:,1:].sum(axis=0).values).reshape(1,len(pivot1.columns)-1),columns=pivot1.columns[1:])
total['Nama Cabang'] ='TOTAL'


df_mie3 = df_mie.merge(df_days, how='left')
#df_mie3['AVG_SALES'] = df_mie3['QTY'] / df_mie3['days'] 
df_mie3['AVG_SALES(-Cancel nota)'] = df_mie3['Kuantitas'] / df_mie3['days'] 

df_mie3['Tanggal'] = pd.to_datetime(df_mie3['BULAN'], format='%b %Y')
df_mie3['BULAN'] = pd.Categorical(df_mie3['BULAN'], categories=df_mie3.sort_values('Tanggal')['BULAN'].unique(), ordered=True)

pivot2 = df_mie3[(df_mie3['BULAN'].str.contains('2024')) & (df_mie3['Kuantitas']>0)].pivot(index='CABANG',columns='BULAN',values='AVG_SALES(-Cancel nota)').reset_index()
avg = pd.DataFrame((pivot2.iloc[:,1:].mean(axis=0).values).reshape(1,len(pivot2.columns)-1),columns=pivot2.columns[1:])
avg['CABANG']='AVG DAILY'+(pivot2['CABANG'].str.len().max()+22)*' '

df_mie = df_mie.merge(df_days, how='left')
df_mie['AVG_SALES(-Cancel nota)'] = df_mie['Kuantitas'] / df_mie['days'] 

df_mie2 = df_mie[df_mie['Kuantitas']!=0].groupby('BULAN')[['Nama Cabang']].nunique().rename(columns={'Nama Cabang':'Total Cabang'}).reset_index().merge(df_mie[df_mie['AVG_SALES(-Cancel nota)']>=4400].groupby(['BULAN'])[['Nama Cabang']].nunique().reset_index().rename(columns={'Nama Cabang':'Total Cabang Achieve'}), how='left'    
)
df_mie2['%'] = round((df_mie2['Total Cabang Achieve'] / df_mie2['Total Cabang']) *100,2)

df_mie2 = df_mie2[df_mie2['BULAN'].str.contains('2024')]

df_mie2['Tanggal'] = pd.to_datetime(df_mie2['BULAN'], format='%b %Y')
df_mie2['BULAN'] = pd.Categorical(df_mie2['BULAN'], categories=df_mie2.sort_values('Tanggal')['BULAN'].unique(), ordered=True)
df_mie2 = df_mie2.sort_values('BULAN').T


grafik_tab, data_tab, = st.tabs(["GRAFIK", "DATA"])
with grafik_tab:
    col_1 = st.columns(4)
    with col_1[0]:
        st.write('')
    with col_1[1]:
        st.text(' ')
        st.text(' ')
        st.metric(label="Total Sales (Qty)", value=f'{pivot1.iloc[:,-1].sum():,.0f}', delta=f"{(pivot1.iloc[:,-1].sum()-pivot1.iloc[:,-2].sum())/pivot1.iloc[:,-2].sum()*100:.2f}%", delta_color="normal")
    with col_1[2]:
        st.text(' ')
        st.text(' ')
        st.metric(label="Total Cabang", value=f'{pivot1[pivot1[pivot1.columns[-1]]>0].iloc[:,-1].count()}', delta=int(pivot1[pivot1[pivot1.columns[-1]]>0].iloc[:,-1].count()-pivot1[pivot1[pivot1.columns[-2]]>0].iloc[:,-2].count()), delta_color="normal")
    with col_1[3]:
        st.text(' ')
        st.text(' ')
        st.metric(label="Avg. Daily Sales", value=f'{avg.iloc[:,-2].sum():,.2f}', delta=f"{(avg.iloc[:,-2].sum()-avg.iloc[:,-3].sum())/avg.iloc[:,-3].sum()*100:.2f}%", delta_color="normal")
    
    style_metric_cards(background_color='#143d59',border_left_color='#FFFFFF',border_size_px=0)

    fig = create_dual_axis_chart(df_mie2.T.iloc[:,:2].merge(total.iloc[:,:-1].T,how='left',on='BULAN').rename(columns={0:'Total Sales'})
    , 'BULAN', 'Total Sales', 'Total Cabang',' ')
    with stylable_container(
        key='grafik1',
        css_styles="""
            {   background-color: white;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
        st.plotly_chart(fig)#, use_container_width=True)
    

with data_tab:
    AgGrid(pivot1,
    gridOptions=grid_options,  fit_columns_on_grid_load=False, width='100%',
    allow_unsafe_jscode=True)
    
    st.dataframe(total.loc[:,[total.columns[-1]]+total.columns[:-1].to_list()], use_container_width=True, hide_index=True)
    st.dataframe(avg.loc[:,[avg.columns[-1]]+avg.columns[:-1].to_list()], use_container_width=True, hide_index=True)
    
    df_mie2.columns = df_mie2.iloc[0,:]
    st.dataframe(df_mie2.iloc[[1,2,3],:].reset_index().rename(columns={'index':'BULAN'}), use_container_width=True, hide_index=True)


css = '''
<style>
    .stTabs [data-baseweb="tab-highlight"] {
        background-color:white;
        color:#FFFFFF;
    }
	.stTabs [data-baseweb="tab-list"] {
		gap: 6px;
  		border-bottom: 2px solid #143d59;
    }

	.stTabs [data-baseweb="tab"] {
		height: 30px;
  		border-radius: 10px 10px 0 0;
        color: white;
        white-space: pre-wrap;
		background-color: #143d59;
		border-radius: 0px 0px 0px 0px;
		gap: 1px;
  		padding-right: 10px;
      		padding-left: 10px;
		padding-top: 0px;
		padding-bottom: 0px;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)


