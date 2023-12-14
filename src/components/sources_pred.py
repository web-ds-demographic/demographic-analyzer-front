import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from http_req.api_requests import get_source_names, get_regions_by_source, get_minmax_date, post_demography_prediction
from http_req.process_data import find_key_by_value
from io import BytesIO
import re

async def fetch_data():
    with st.spinner('Загрузка...'):
        sources = await get_source_names()
        selected_source = st.selectbox("Выберите источник из доступных:", sources)
        
        if selected_source != 'source':
            regions = await get_regions_by_source(selected_source)
            selected_region = st.selectbox("Выберите регион из доступных:", list(regions.values()))
            selected_region = find_key_by_value(regions, selected_region)
            variant = st.radio( "Выберите вид прогнозирования:", ["Ретростпективное", "Обычное"],
            captions = ["Выбрать определенный период прогнозирования", "Выбрать весь период"])
            minmax_date = await get_minmax_date(selected_region, selected_source)
            data = None
            years_to_forecast = None
            if minmax_date is None:
                st.markdown(f"Извините. Данная страна недоступна!")
            else:
                if variant=="Обычное": 
                    st.markdown(f"Данные будут проанализованы на доступных датах **{minmax_date['start']}** - **{minmax_date['end']}**")
                    years_to_forecast = int(st.number_input("Введите количество лет для прогнозирования", value=5, placeholder="Введите число..."))

                if variant=="Ретростпективное":
                    start_year = int(re.search(r'\d{4}', minmax_date["start"]).group())
                    end_year = int(re.search(r'\d{4}', minmax_date["end"]).group())
                    period_of_prediction = st.slider('Miles', min_value=start_year, max_value=end_year, value=[start_year, end_year])
                    minmax_date = {"start":f"{period_of_prediction[0]}-01-01", "end":f"{period_of_prediction[1]}-01-01"}
                    st.markdown(f"Данные будут проанализованы на выбранных датах **{minmax_date['start']}** - **{minmax_date['end']}**")
                    years_to_forecast = int(st.number_input("Введите количество лет для прогнозирования", value=5, placeholder="Введите число..."))

                    
            
            data = {
                "region": selected_region,
                "source": selected_source,
                "predict_years_count": years_to_forecast,
                "inputDataPeriod": minmax_date,
            }

            return data
        else:
            st.warning("Выберите источник данных.", icon="⚠️")
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
                df.to_excel(excel_data, index=False)
                excel_data.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name="forecast_data.xlsx",
                    key="download-excel"
                )
            
            minmax_date = await get_minmax_date(data["region"], data["source"])
            minmax_date["start"] = data['inputDataPeriod']["end"]
            _, tdata = await post_demography_prediction({
                "region": data["region"],
                "source": data["source"],
                "predict_years_count": 0,
                "inputDataPeriod": minmax_date,
            })
            try:
                df_acc = pd.DataFrame(tdata)

                merged_df = pd.merge(df, df_acc, on='Year', suffixes=('_df', '_df_acc'))

                merged_df['Accuracy(%)'] = (1 - abs(merged_df['N(t)_df_acc'] - merged_df['N(t)_df']) / merged_df['N(t)_df_acc']) * 100

                error_df = merged_df[['Year', 'Accuracy(%)']].copy()
                with st.expander("Точноть прогнозирования в %"):
                    st.dataframe(error_df, use_container_width=True)
            except:
                st.warning("Точность не может быть вычислена для прогнозирования на будущее!")

            


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
            
            await visualize_data(df, selected_plot_type)
        else:
            st.warning("Введите данные!")