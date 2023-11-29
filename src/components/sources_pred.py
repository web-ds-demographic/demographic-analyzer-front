import streamlit as st
import pandas as pd
import plotly.express as px
from test_data.alg import get_pred

def run_source_prediction():
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

    # Выбор отображаемых столбцов
    selected_columns = st.multiselect("Выберите столбцы для отображения:", result.columns)

    # Информация о столбцах
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
        'Qt': 'Показатель изменчивости'
    }

    # Отображение информации о столбцах
    for col in selected_columns:
        st.write(f"**{col}**: {column_info.get(col, 'Нет информации')}")


    st.subheader("Результат прогнозирования:")
    st.write(result.set_index('Year'))
    fig = px.line(result, x='Year', y=selected_columns, title='Прогноз демографических данных')
    fig.update_layout(width=900, height=500, xaxis_title='Год', yaxis_title='Значение')
    st.plotly_chart(fig)