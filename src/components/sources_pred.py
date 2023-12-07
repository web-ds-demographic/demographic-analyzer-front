import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
from local_processing.alg import get_pred
from http_req.api_requests import get_source_names, get_regions_by_source, get_minmax_date, post_demography_prediction



def run_source_prediction():
    sources = get_source_names()
    check = True
    selected_source = st.selectbox("Выберите источник из доступных:", sources)
    if selected_source != 'sources': check = False
    if selected_source:
        regions = get_regions_by_source(selected_source)
        selected_region = st.selectbox("Выберите регион из доступных:", regions, disabled=check)
    
    minmax_date = get_minmax_date(selected_region, selected_source)
    st.markdown(f"Данные будут проанализованы на доступных датах {minmax_date}")

    years_to_forecast = int(st.number_input("Введите количество лет для прогнозирования", value=5, placeholder="Введите число..."))
    data = {    # dict тип
        "region": selected_region,          
        "source": selected_source,
        "predict_years_count": years_to_forecast,
        "inputDataPeriod": minmax_date,
    }
    # получение прогноза
    response_status, forecast = post_demography_prediction(data)
    df = None
    try:
        if response_status == 200:
            df = pd.DataFrame(forecast)
            # удаление столбца 'index' и 'qt, если он есть
            df = df.drop(columns=['index','Qt'], errors='ignore')
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Введите данные!")
    

        plot_types = ['Линейный график', 'Точечный график']
        selected_plot_type = st.selectbox("Выберите тип графика:", plot_types)

        fig = sp.make_subplots(rows=len(df.columns)-1 // 2 + 1, cols=2, subplot_titles=df.columns[1:])
        row, col = 1, 1

        for col_name in df.columns[1:]:
            if selected_plot_type == 'Линейный график':
                fig.add_trace(go.Scatter(x=df['Year'], y=df[col_name], mode='lines', name=col_name),
                            row=row, col=col)
            else:
                fig.add_trace(go.Scatter(x=df['Year'], y=df[col_name], mode='markers', name=col_name),
                            row=row, col=col)
            col += 1
            if col > 2:
                col = 1
                row += 1

        fig.update_layout(width=900, height=500 * (len(df.columns) // 2 + 1), showlegend=False)
        fig.update_xaxes(title_text='Год')
        fig.update_yaxes(title_text='Значение')

        st.plotly_chart(fig)
    except:
        st.write("Error...")
        