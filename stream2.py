import streamlit as st
import pandas as pd
import numpy as np

# Simulasi DataFrame
data = pd.DataFrame({
    "Metric": ["Revenue", "Visitors", "Profit", "Users"],
    "Value": [5000, 3500, 2000, 1200],
    "Change": [500, -200, 250, 100]
})

# Menampilkan metrik berdasarkan data
for index, row in data.iterrows():
    st.metric(label=row["Metric"], value=f"${row['Value']}", delta=f"{row['Change']}")
