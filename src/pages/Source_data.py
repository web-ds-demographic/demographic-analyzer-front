import streamlit as st
import pandas as pd
import plotly.express as px

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


st.title("Анализ демографических данных")

countries = ["Senegal", "Russia"]
selected_country = st.selectbox("Выберите страну из доступных:", countries)


if selected_country == "Senegal":
    file_path = "./test_data/senegal.csv"
else:
    file_path = "./test_data/russia.csv"

df = pd.read_csv(file_path)

st.subheader("Исходные данные:")
st.write(df)

fig = px.line(df, x='Year', y=df.columns[1:], title='Прогноз демографических данных')
fig.update_layout(width=900, height=500, xaxis_title='Год', yaxis_title='Значение')
st.plotly_chart(fig)

