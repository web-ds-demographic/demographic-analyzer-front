import streamlit as st

st.set_page_config(page_title="DemografiX", page_icon=":bar_chart:", layout="wide")

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

# Заголовок и информация о создателях
st.markdown(
    """
    ###### Created by DemografiX team 
    ---
    # Сервис по анализу мировых демографических процессов
    """
)
st.write(
    "Проект **DemografiX** - это веб-ориентированное приложение, предназначенное для анализа динамики мировых демографических процессов и прогнозирования изменений в демографических показателях. "
    "Этот проект представляет собой инструмент для исследователей, аналитиков, которые интересуются демографией и желают более точно понимать и анализировать динамику населения."
)

st.title("Проект DemografiX")
st.image("./assets/hmpg.png", use_column_width=False)


st.subheader("Контакты")
st.write("Email: savchenckoilia@gmail.com")
st.write("Telegram: @bgsnqkik")

