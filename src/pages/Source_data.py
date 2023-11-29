import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go

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

st.title(":chart_with_upwards_trend: Исходные демографические данные")

countries = ["Senegal", "Russia"]
selected_country = st.selectbox("Выберите страну из доступных:", countries)
st.markdown(
        """
        ###
        | Year | N(t) | B(t) | D(t) | NM(t) |
        |------|------|------|------|-------|
        | ...  | ...  | ...  | ...  |   ... |

        где:

        N(t): Количество населения

        B(t): Количество рожденных

        NM(t): Количество миграций

        D(t): Количество смертей

        """
)

if selected_country == "Senegal":
    file_path = "./test_data/senegal.csv"
else:
    file_path = "./test_data/russia.csv"

df = pd.read_csv(file_path)

st.subheader("Исходные данные:")
st.dataframe(df, use_container_width=True)

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
