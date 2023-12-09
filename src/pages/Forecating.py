import asyncio
import streamlit as st
import pandas as pd
import plotly.express as px
from components.file_pred import run_file_prediction
from components.sources_pred import run_source_prediction
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title(":chart_with_upwards_trend: Прогнозирование демографических данных")



selected_option = st.selectbox("Выберите способ:", ["Использовать имеющиеся источники для стран", "Загрузка файла"])
if selected_option == "Использовать имеющиеся источники для стран":
    asyncio.run(run_source_prediction())
if selected_option == "Загрузка файла":
    asyncio.run(run_file_prediction())
