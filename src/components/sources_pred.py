import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from http_req.api_requests import get_source_names, get_regions_by_source, get_minmax_date, post_demography_prediction
from http_req.process_data import find_key_by_value, get_country_names_by_iso2
from io import BytesIO

async def fetch_data():
    with st.spinner('Загрузка...'):
        sources = await get_source_names()
        selected_source = st.selectbox("Выберите источник из доступных:", sources)
        
        if selected_source != 'source':
            regions = await get_regions_by_source(selected_source)
            reg_full = get_country_names_by_iso2(regions)
            selected_region = st.selectbox("Выберите регион из доступных:", list(reg_full.values()))
            selected_region = find_key_by_value(reg_full, selected_region)

            minmax_date = await get_minmax_date(selected_region, selected_source)
            if minmax_date is None:
                st.markdown(f"Извините. Данная страна недоступна!")
            else:
                st.markdown(f"Данные будут проанализованы на доступных датах {minmax_date}")

            years_to_forecast = int(st.number_input("Введите количество лет для прогнозирования", value=5, placeholder="Введите число..."))
            
            data = {
                "region": selected_region,
                "source": selected_source,
                "predict_years_count": years_to_forecast,
                "inputDataPeriod": minmax_date,
            }

            return data
        else:
            st.warning("Выберите источник данных.")
            return None
        


async def visualize_data(df, selected_plot_type):

    selected_columns = st.multiselect("Выберите столбцы для отображения:", df.columns[1:])

    for col_name in selected_columns:
        unique_key = f"{col_name}_{selected_plot_type}"  # Уникальный ключ для каждого виджета
        trace = go.Scatter(x=df['Year'], y=df[col_name], mode='lines' if selected_plot_type == 'Линейный график' else 'markers', name=col_name)
        st.plotly_chart(go.Figure(trace).update_layout(title=f'{col_name} - {selected_plot_type}', xaxis_title='Год', yaxis_title='Значение'), key=unique_key, width=1400, height=800)


async def run_source_prediction():
    data = await fetch_data()

    if data:
        response_status, forecast = await post_demography_prediction(data)
        
        if response_status == 200:
            df = pd.DataFrame(forecast)
            df = df.drop(columns=['index', 'Qt'], errors='ignore')
            
            st.dataframe(df, use_container_width=True)

            col1, col2 = st.columns([1,1])
            with col1:
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False),
                    file_name="forecast_data.csv",
                    key="download-csv"
                )
            with col2:
                excel_data = BytesIO()
                df.to_excel(excel_data, index=False)  # Removed engine='xlsxwriter'
                excel_data.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name="forecast_data.xlsx",
                    key="download-excel"
                )
            
            
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
            
            # Display graph
            await visualize_data(df, selected_plot_type)
        else:
            st.warning("Введите данные!")