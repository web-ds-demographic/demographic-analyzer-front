import asyncio
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from http_req.api_requests import get_source_names, get_regions_by_source, get_minmax_date, post_demography_prediction
from http_req.process_data import find_key_by_value

async def run_source_data():
    st.title(":chart_with_upwards_trend: Исходные данные источников")
    sources = await get_source_names()
    selected_source = st.selectbox("Выберите источник из доступных:", sources)
    data = None
    if selected_source != 'source':
        regions = await get_regions_by_source(selected_source)
        selected_region = st.selectbox("Выберите регион из доступных:", list(regions.values()))
        selected_region = find_key_by_value(regions, selected_region)

        minmax_date = await get_minmax_date(selected_region, selected_source)
        if minmax_date is None:
            st.markdown(f"Извините. Данная страна недоступна!")
        else:
            st.markdown(f"Доступные промежуток данных **{minmax_date['start']}** - **{minmax_date['end']}**")

        minmax_date = await get_minmax_date(selected_region, selected_source)
        
        data = {
            "region": selected_region,
            "source": selected_source,
            "predict_years_count": 0,
            "inputDataPeriod": minmax_date,
        }

    else:
        st.warning("Выберите источник данных.")

    if data:
        response_status, forecast = await post_demography_prediction(data)
        
        if response_status == 200:
            df = pd.DataFrame(forecast)
            df = df.drop(columns=['index', 'Qt'], errors='ignore')
            st.dataframe(df, use_container_width=True)
            
            with st.expander(":information_source: Информация"):
                st.markdown("""
                | Столбец  | Описание                                |
                |----------|-----------------------------------------|
                | N(t)     | Количество населения                    |
                | B(t)     | Рождаемость                             |
                | NM(t)    | Количество миграций                     |
                | D(t)     | Количество смертей                      |
                | DNM      | Смерти + миграции                       |
                | IntB     | Сумма рождаемости за все время          |
                | IntDNM   | Сумма (Смерти + миграции) за все время  |
                | rBt      | Процентный прирост рождаемости          |
                | rDNMt    | Процентный прирост (Смерти + миграции)  |
                """)
            selected_plot_type = st.selectbox("Выберите тип графика:", ['Линейный график', 'Точечный график'])
            selected_columns = st.multiselect("Выберите столбцы для отображения:", df.columns[1:])

            for col_name in selected_columns:
                unique_key = f"{col_name}_{selected_plot_type}"  # Уникальный ключ для каждого виджета
                trace = go.Scatter(x=df['Year'], y=df[col_name], mode='lines' if selected_plot_type == 'Линейный график' else 'markers', name=col_name)
                st.plotly_chart(go.Figure(trace).update_layout(title=f'{col_name} - {selected_plot_type}', xaxis_title='Год', yaxis_title='Значение'), key=unique_key)
        else:
            st.warning("Введите данные!")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

asyncio.run(run_source_data())