import streamlit as st
import pandas as pd
import plotly.express as px
from test_data.alg import get_pred

            
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


st.title("Прогнозирование демографических данных")

countries = ["Senegal", "Russia"]
selected_country = st.selectbox("Выберите страну из доступных:", countries)


if selected_country == "Senegal":
    file_path = "./test_data/senegal.csv"
else:
    file_path = "./test_data/russia.csv"

df = pd.read_csv(file_path)

years_to_forecast = st.slider("Выберите количество лет для прогнозирования:", 1, 30, 5)

# Получение прогноза
result = get_pred(df, years_to_forecast)

st.subheader("Результат прогнозирования:")
st.write(result.set_index('Year'))
fig = px.line(result, x='Year', y=result.columns[1:], title='Прогноз демографических данных')
fig.update_layout(width=900, height=500, xaxis_title='Год', yaxis_title='Значение')
st.plotly_chart(fig)
# st.linechart(result.set_index('Year'), width=900, height=500, use_container_width=True)