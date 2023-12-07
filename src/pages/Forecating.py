import streamlit as st
import pandas as pd
import plotly.express as px
from components.file_pred import run_file_prediction
from components.sources_pred import run_source_prediction

# Стилизация страницы
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

column_info = {
    'N(t)': 'Количество населения',
    'B(t)': 'Рождаемость',
    'NM(t)': 'Количество миграций',
    'D(t)': 'Количество смертей',
    'DNM': 'Смерти + миграции',
    'IntB': 'Сумма рождаемости за все время',
    'IntDNM': 'Сумма (Смерти + миграции) за все время',
    'rBt': 'Процентный прирост рождаемости',
    'rDNMt': 'Процентный прирост (Смерти + миграции)',
}


st.title(":chart_with_upwards_trend: Прогнозирование демографических данных")
selected_option = st.selectbox("Выберите способ:", ["Использовать имеющиеся источники для стран", "Загрузка файла"])
if selected_option == "Использовать имеющиеся источники для стран":
    run_source_prediction()
if selected_option == "Загрузка файла":
    run_file_prediction()


    
        

        

