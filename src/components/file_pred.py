import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.express as px
from local_processing.alg import get_pred

def run_file_prediction():
    uploaded_file = st.file_uploader("Выберите .csv файл")
    st.markdown(
        """
        ### Какой входной файл должен иметь вид и формат?
        Формат .csv
        | Year | N(t) | B(t) | D(t) | NM(t) |
        |------|------|------|------|-------|
        | 1970 |  100 |   50 |   40 |   10  |
        | 1971 |  105 |   55 |   45 |   15  |
        | ...  | ...  | ...  | ...  |   ... |

        где:

        N(t): Количество населени,

        B(t): Количество рожденных,

        NM(t): Количество миграций,

        D(t): Количество смертей

        """
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        years_to_forecast = int(st.number_input("Введите количество лет для прогнозирования", value=5, placeholder="Введите число..."))

        result = get_pred(df, years_to_forecast)
        result = result.drop(columns=['Qt'])

        selected_columns = st.multiselect("Выберите столбцы для отображения:", result.columns, default="N(t)")

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

        for col in selected_columns:
            st.write(f"**{col}**: {column_info.get(col, 'Нет информации')}")

            # создание графика для каждого выбранного столбца
            chart_type = st.selectbox(f"Выберите вид отображения для {col}:", ["Линейный график", "Точечный график"])
            fig = px.line(result, x='Year', y=col, title=f'Прогноз {column_info.get(col, "Данные")}')
            if chart_type == "Точечный график":
                fig.update_traces(mode='markers')

            fig.update_layout(width=900, height=500, xaxis_title='Год', yaxis_title='Значение')
            st.plotly_chart(fig)
