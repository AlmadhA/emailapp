import streamlit as st

if st.button("Page 1"):
    st.switch_page("https://dashboard-harga-barang.streamlit.app/")
create_page = st.Page("stream.py", title="Create entry", icon=":material/add_circle:")
delete_page = st.Page("stream2.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([create_page, delete_page])

st.page_link("https://dashboard-harga-barang.streamlit.app/",label="Home")
with st.sidebar:
  with st.expander('Dashboard'):
    st.markdown(
        "<a href='https://dashboard-harga-barang.streamlit.app/' target='_self' style='text-decoration:none;'>"
        "<div style='background-color:#982B1C;padding:20px;text-align:center;border-radius:10px;color:black; font-family:Roboto,sans-serif; font-size: 16px;'>"
        "<strong style='color:white;'>Analisis Harga Barang</strong></div>"
        "</a>",
        unsafe_allow_html=True,
    )
    
    
    st.markdown(
        """
        <a href='https://dashboard-harga-barang.streamlit.app/' onclick="window.location.href=this.href; return false;" style='text-decoration:none;'>
        <div style='background-color:#982B1C;padding:20px;text-align:center;border-radius:10px;color:black; font-family:Roboto,sans-serif; font-size: 16px;'>
        <strong style='color:white;'>Analisis Harga Barang</strong>
        </div>
        </a>
        """,
        unsafe_allow_html=True
    )


